import json
import unittest
from typing import Any, List, NamedTuple
from uuid import UUID

from notbank_python_sdk.client_connection import ClientConnection, RequestType
from notbank_python_sdk.core.endpoint_category import EndpointCategory
from notbank_python_sdk.core.response_handler import ResponseHandler
from notbank_python_sdk.error import NotbankException
from notbank_python_sdk.models.verification_status import VerificationLevel, VerificationProcessResult, VerificationStatus
from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.parsing import parse_response_fn
from notbank_python_sdk.requests_models import GetVerificationStatusRequest


ENDPOINT = "v2/account/verification/status"
USER_ID = UUID("3f2504e0-4f89-41d3-9a0c-0305e82c3301")
PROCESS_ID = "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"

FULL_STATUS = {
    "id": PROCESS_ID,
    "locked": False,
    "next_level": "trader_plus",
    "last_previous_status": "rejected",
    "last_previous_reason": "verification_expired",
    "is_business": False,
    "verification_tier": 2,
}

EMPTY_STATUS = {
    "id": None,
    "locked": True,
    "next_level": None,
    "last_previous_status": None,
    "last_previous_reason": None,
    "is_business": True,
    "verification_tier": 4,
}


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


class GetVerificationStatusTestCase(unittest.TestCase):
    def test_uses_v2_endpoint_nb_category_and_get(self):
        stub = StubConnection(FULL_STATUS)
        client = NotbankClient(stub.as_client_connection())

        client.get_verification_status(GetVerificationStatusRequest())

        self.assertEqual(len(stub.calls), 1)
        call = stub.last_call
        self.assertEqual(call.request_type, RequestType.GET)
        self.assertEqual(call.endpoint, ENDPOINT)
        self.assertIs(call.endpoint_category, EndpointCategory.NB)
        self.assertEqual(call.endpoint_category.val, "api/nb")

    def test_sends_user_id_as_string(self):
        stub = StubConnection(FULL_STATUS)
        client = NotbankClient(stub.as_client_connection())

        client.get_verification_status(
            GetVerificationStatusRequest(user_id=USER_ID))

        self.assertEqual(stub.last_call.request_data,
                         {"user_id": str(USER_ID)})

    def test_omits_user_id_when_none(self):
        stub = StubConnection(FULL_STATUS)
        client = NotbankClient(stub.as_client_connection())

        client.get_verification_status()

        # to_nb_dict drops the None fields, so the server answers for the
        # authenticated user.
        self.assertEqual(stub.last_call.request_data, {})

    def test_parses_all_fields(self):
        stub = StubConnection(FULL_STATUS)
        client = NotbankClient(stub.as_client_connection())

        response = client.get_verification_status()

        self.assertIsInstance(response, VerificationStatus)
        self.assertEqual(response.id, PROCESS_ID)
        self.assertFalse(response.locked)
        self.assertIs(response.next_level, VerificationLevel.TRADER_PLUS)
        self.assertIs(response.last_previous_status,
                      VerificationProcessResult.REJECTED)
        self.assertEqual(response.last_previous_reason, "verification_expired")
        self.assertFalse(response.is_business)
        self.assertEqual(response.verification_tier, 2)

    def test_parses_null_fields(self):
        # v2 answers 200 with a null id when there is no pending process,
        # instead of the 404 of v1.
        stub = StubConnection(EMPTY_STATUS)
        client = NotbankClient(stub.as_client_connection())

        response = client.get_verification_status()

        self.assertIsNone(response.id)
        self.assertTrue(response.locked)
        self.assertIsNone(response.next_level)
        self.assertIsNone(response.last_previous_status)
        self.assertIsNone(response.last_previous_reason)
        self.assertTrue(response.is_business)
        self.assertEqual(response.verification_tier, 4)

    def test_ignores_unknown_keys(self):
        stub = StubConnection(dict(FULL_STATUS, current_process_data={}))
        client = NotbankClient(stub.as_client_connection())

        response = client.get_verification_status()

        self.assertEqual(response.id, PROCESS_ID)
        self.assertFalse(hasattr(response, "current_process_data"))

    def test_unwraps_envelope(self):
        envelope = {"status": "success", "data": FULL_STATUS}

        response = ResponseHandler.handle_nb_response(
            FakeResponse(envelope),
            parse_response_fn(VerificationStatus, from_pascal_case=False),
            EndpointCategory.NB)

        self.assertEqual(response.id, PROCESS_ID)
        self.assertIs(response.next_level, VerificationLevel.TRADER_PLUS)

    def test_raises_on_error_status(self):
        envelope = {"status": "error", "message": "user not found"}

        with self.assertRaises(NotbankException):
            ResponseHandler.handle_nb_response(
                FakeResponse(envelope, 404),
                parse_response_fn(VerificationStatus, from_pascal_case=False),
                EndpointCategory.NB)


if __name__ == "__main__":
    unittest.main()
