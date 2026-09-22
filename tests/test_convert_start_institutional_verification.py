import json
import unittest
from typing import Any, List, NamedTuple

from notbank_python_sdk.client_connection import ClientConnection, RequestType
from notbank_python_sdk.core.endpoint_category import EndpointCategory
from notbank_python_sdk.core.response_handler import ResponseHandler
from notbank_python_sdk.error import NotbankException
from notbank_python_sdk.models.start_institutional_verification import StartInstitutionalVerificationResponse
from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.parsing import parse_response_fn
from notbank_python_sdk.requests_models.start_institutional_verification_request import StartInstitutionalVerificationRequest


ENDPOINT = "account/verification/institutional"
LINK = "https://sumsub.com/websdk/an-uuid"


class RecordedRequest(NamedTuple):
    request_type: RequestType
    endpoint: str
    endpoint_category: EndpointCategory
    request_data: Any


def _unexpected(name: str):
    def call(*args, **kwargs):
        raise AssertionError("unexpected call to " + name)
    return call


class StubConnection:
    """Records the request done by the client and answers with canned,
    already unwrapped, response data (the envelope unwrapping happens in the
    rest layer, below this point)."""

    def __init__(self, response_data: Any) -> None:
        self._response_data = response_data
        self.calls = []  # type: List[RecordedRequest]

    def _recorder(self, request_type: RequestType):
        def request_fn(endpoint, endpoint_category, request_data, parse_response_fn):
            self.calls.append(RecordedRequest(
                request_type, endpoint, endpoint_category, request_data))
            return parse_response_fn(self._response_data)
        return request_fn

    def as_client_connection(self) -> ClientConnection:
        return ClientConnection(
            post_request=self._recorder(RequestType.POST),
            get_request=self._recorder(RequestType.GET),
            delete_request=self._recorder(RequestType.DELETE),
            subscribe=_unexpected("subscribe"),
            unsubscribe=_unexpected("unsubscribe"),
            authenticate_user=_unexpected("authenticate_user"),
            connect=lambda: None,
            close=lambda: None,
        )

    @property
    def last_call(self) -> RecordedRequest:
        return self.calls[-1]


class FakeResponse:
    """Minimal stand in for requests.Response. The response handler only uses
    json(), status_code and text."""

    def __init__(self, payload: Any, status_code: int = 200) -> None:
        self.status_code = status_code
        self.text = json.dumps(payload)

    def json(self, **kwargs: Any) -> Any:
        return json.loads(self.text, **kwargs)


class StartInstitutionalVerificationTestCase(unittest.TestCase):
    def test_request_is_a_post_to_the_nb_institutional_endpoint(self):
        stub = StubConnection({"link": LINK, "user_id": "an-uuid"})
        client = NotbankClient(stub.as_client_connection())

        client.start_institutional_verification(
            StartInstitutionalVerificationRequest())

        self.assertEqual(len(stub.calls), 1)
        call = stub.last_call
        self.assertEqual(call.request_type, RequestType.POST)
        self.assertEqual(call.endpoint, ENDPOINT)
        self.assertIs(call.endpoint_category, EndpointCategory.NB)
        self.assertEqual(call.endpoint_category.val, "api/nb")

    def test_request_without_arguments_sends_an_empty_payload(self):
        stub = StubConnection({"link": LINK, "user_id": "an-uuid"})
        client = NotbankClient(stub.as_client_connection())

        client.start_institutional_verification()

        # to_nb_dict drops the None fields (see converter._build_factory), so
        # an omitted phone does not reach the payload at all.
        self.assertEqual(stub.last_call.request_data, {})
        self.assertNotIn("phone", stub.last_call.request_data)

    def test_request_sends_phone_as_a_snake_case_key(self):
        stub = StubConnection({"link": LINK, "user_id": "an-uuid"})
        client = NotbankClient(stub.as_client_connection())

        client.start_institutional_verification(
            StartInstitutionalVerificationRequest(phone="+56911111111"))

        self.assertEqual(stub.last_call.request_data,
                         {"phone": "+56911111111"})

    def test_response_is_parsed_from_the_unwrapped_data(self):
        stub = StubConnection({"link": LINK, "user_id": "an-uuid"})
        client = NotbankClient(stub.as_client_connection())

        response = client.start_institutional_verification()

        self.assertIsInstance(response, StartInstitutionalVerificationResponse)
        self.assertEqual(response.link, LINK)
        self.assertEqual(response.user_id, "an-uuid")

    def test_response_with_a_null_link_is_a_valid_success_response(self):
        # The server answers success with a null link when the verification
        # url cannot be retrieved, or when there is no active applicant
        # request: it logs the problem and still returns 200, so the sdk has
        # to parse it instead of blowing up.
        stub = StubConnection({"link": None, "user_id": "an-uuid"})
        client = NotbankClient(stub.as_client_connection())

        response = client.start_institutional_verification()

        self.assertIsInstance(response, StartInstitutionalVerificationResponse)
        self.assertIsNone(response.link)
        self.assertEqual(response.user_id, "an-uuid")

    def test_response_parsing_ignores_unknown_keys(self):
        # The parser is not strict, so an extra key the sdk does not model
        # (such as the 'token' the endpoint used to return) is dropped
        # instead of raising.
        stub = StubConnection(
            {"link": LINK, "user_id": "an-uuid", "token": "tkn-123"})
        client = NotbankClient(stub.as_client_connection())

        response = client.start_institutional_verification()

        self.assertEqual(response.link, LINK)
        self.assertEqual(response.user_id, "an-uuid")
        self.assertFalse(hasattr(response, "token"))

    def test_response_handler_unwraps_the_nb_envelope(self):
        envelope = {
            "status": "success",
            "data": {"link": LINK, "user_id": "an-uuid"}}

        response = ResponseHandler.handle_nb_response(
            FakeResponse(envelope),
            parse_response_fn(
                StartInstitutionalVerificationResponse, from_pascal_case=False),
            EndpointCategory.NB)

        self.assertEqual(response.link, LINK)
        self.assertEqual(response.user_id, "an-uuid")

    def test_response_handler_unwraps_an_envelope_with_a_null_link(self):
        envelope = {
            "status": "success",
            "data": {"link": None, "user_id": "an-uuid"}}

        response = ResponseHandler.handle_nb_response(
            FakeResponse(envelope),
            parse_response_fn(
                StartInstitutionalVerificationResponse, from_pascal_case=False),
            EndpointCategory.NB)

        self.assertIsNone(response.link)
        self.assertEqual(response.user_id, "an-uuid")

    def test_response_handler_raises_on_an_error_status(self):
        envelope = {"status": "error", "message": "invalid_request"}

        with self.assertRaises(NotbankException):
            ResponseHandler.handle_nb_response(
                FakeResponse(envelope, 400),
                parse_response_fn(
                    StartInstitutionalVerificationResponse, from_pascal_case=False),
                EndpointCategory.NB)


if __name__ == "__main__":
    unittest.main()
