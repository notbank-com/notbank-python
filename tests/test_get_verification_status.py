import os
import unittest
from uuid import UUID

from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.requests_models import GetVerificationStatusRequest

from tests import test_helper


# keys.json UserId is the alphapoint (int) user id, while this endpoint takes
# the notbank user uuid, so it comes from the environment instead.
USER_UUID_ENV = "NOTBANK_TEST_USER_UUID"


class TestGetVerificationStatus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, credentials)
        cls.client = NotbankClient(connection)

    def test_get_verification_status(self):
        response = self.client.get_verification_status()
        self.assertIsInstance(response.locked, bool)
        self.assertIsInstance(response.verification_tier, int)

    def test_get_verification_status_with_user_id(self):
        user_uuid = os.environ.get(USER_UUID_ENV)
        if user_uuid is None:
            self.skipTest(USER_UUID_ENV + " is not set")
        response = self.client.get_verification_status(
            GetVerificationStatusRequest(user_id=UUID(user_uuid)))
        self.assertIsInstance(response.locked, bool)


if __name__ == "__main__":
    unittest.main()
