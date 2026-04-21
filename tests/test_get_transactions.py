from uuid import UUID

import unittest

from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.requests_models import GetTransactionsRequest
from notbank_python_sdk.constants import WalletTransactionType, WalletTransactionSubType

from tests import test_helper


class TestGetTransactions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)

    def test_get_transactions(self):
        response = self.client.get_transactions(GetTransactionsRequest())
        self.assertIsNotNone(response)


    def test_get_transactions_deposit(self):
        response = self.client.get_transactions(GetTransactionsRequest(
            page=1,
            page_size=5,
            type=WalletTransactionType.DEPOSIT,
        ))
        self.assertIsNotNone(response)

    def test_get_transactions_withdraw(self):
        response = self.client.get_transactions(GetTransactionsRequest(
            page=1,
            page_size=5,
            type=WalletTransactionType.WITHDRAW,
            sub_type=WalletTransactionSubType.WITHDRAW,
        ))
        self.assertIsNotNone(response)

    def test_get_transactions_trade(self):
        response = self.client.get_transactions(GetTransactionsRequest(
            page=1,
            page_size=5,
            type=WalletTransactionType.TRADE,
        ))
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()
