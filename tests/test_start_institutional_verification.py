import unittest

from notbank_python_sdk.models.start_institutional_verification import StartInstitutionalVerificationResponse
from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.requests_models import StartInstitutionalVerificationRequest
from tests import test_helper


class TestStartInstitutionalVerification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)

    def test_start_institutional_verification(self):
        response = self.client.start_institutional_verification(
            StartInstitutionalVerificationRequest())
        self.assertIsNotNone(response)
        self.assertIsInstance(response, StartInstitutionalVerificationResponse)
        self.assertIsNotNone(response.token)
        self.assertIsNotNone(response.user_id)


if __name__ == "__main__":
    unittest.main()
