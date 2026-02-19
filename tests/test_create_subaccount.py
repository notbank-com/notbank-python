import unittest

from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.requests_models import CreateSubaccountRequest

from tests import test_helper


class TestCreateSubaccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)

    def test_create_subaccount(self):
        self.client.create_subaccount(
            CreateSubaccountRequest(alias="testsubaccount"))


if __name__ == "__main__":
    unittest.main()
