import unittest

from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.requests_models import GetOneStepWithdrawRequest

from tests import test_helper


class TestGetOneStepWithdraw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)

    def test_get_one_step_withdraw(self):
        response = self.client.get_one_step_withdraw(
            GetOneStepWithdrawRequest(account_id=self.credentials.account_id)
        )
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()
