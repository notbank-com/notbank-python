import unittest
from uuid import UUID

from notbank_python_sdk.client_connection import RequestType
from notbank_python_sdk.core.endpoint_category import EndpointCategory
from notbank_python_sdk.core.response_handler import ResponseHandler
from notbank_python_sdk.error import ErrorCode, NotbankException
from notbank_python_sdk.models.verification_status import VerificationLevel, VerificationProcessResult, VerificationStatus
from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.parsing import parse_response_fn
from notbank_python_sdk.requests_models import GetVerificationStatusRequest

from tests.stub_connection import FakeResponse, StubConnection


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

    def test_raises_notbank_exception_on_unknown_enum_value(self):
        # A level the sdk does not know yet must not leak dacite's ValueError
        # to the caller.
        envelope = {
            "status": "success",
            "data": dict(FULL_STATUS, next_level="a_new_level")}

        with self.assertRaises(NotbankException) as context:
            ResponseHandler.handle_nb_response(
                FakeResponse(envelope),
                parse_response_fn(VerificationStatus, from_pascal_case=False),
                EndpointCategory.NB)

        self.assertIs(context.exception.code, ErrorCode.INVALID_RESPONSE)
        self.assertIn("a_new_level", str(context.exception))

    def test_raises_notbank_exception_on_wrong_value_type(self):
        # A field with an unexpected type must not leak dacite's
        # WrongTypeError to the caller.
        envelope = {
            "status": "success",
            "data": dict(FULL_STATUS, locked="yes")}

        with self.assertRaises(NotbankException) as context:
            ResponseHandler.handle_nb_response(
                FakeResponse(envelope),
                parse_response_fn(VerificationStatus, from_pascal_case=False),
                EndpointCategory.NB)

        self.assertIs(context.exception.code, ErrorCode.INVALID_RESPONSE)
        self.assertIn("locked", str(context.exception))


if __name__ == "__main__":
    unittest.main()
