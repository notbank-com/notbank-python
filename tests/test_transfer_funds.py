from decimal import Decimal
import unittest
from uuid import UUID
from notbank_python_sdk.requests_models.create_fiat_deposit_request import CreateFiatDepositRequest
from notbank_python_sdk.requests_models.get_account_info_request import GetAccountInfoRequest
from notbank_python_sdk.requests_models.transfer_funds_request import TransferFundsRequest

from tests import test_helper

from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.requests_models.get_banks_request import GetBanksRequest


class TestTransferFunds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)

    def test_transfer_funds(self):
        response = self.client.transfer_funds(TransferFundsRequest(
            sender_account_id=72,
            receiver_account_id=69,
            currency_name="USDT",
            amount=Decimal("1"),
            otp="735463",
            notes="a test transfer",
            
        ))
        self.assertIsNotNone(response)

    def test_transfer_funds_caas_user(self):
        response = self.client.transfer_funds(TransferFundsRequest(
            sender_account_id=1151,
            receiver_account_id=69,
            currency_name="USDT",
            amount=Decimal("1"),
            otp="699082",
            notes="a test transfer with caas user",
            user_id=UUID("8d9f2c00-e82a-4ec6-ba2e-7a4356351623"),
        ))
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()
