import unittest

from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.requests_models.get_account_info_request import GetAccountInfoRequest
from notbank_python_sdk.requests_models.get_account_settlement_position_request import GetAccountSettlementPositionsRequest
from tests import test_helper


class TestGetAccountSettlementPositions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection()
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)

    def test_get_account_settlement_positions(self):
        self.client.get_account_settlement_positions(GetAccountSettlementPositionsRequest(
            account_id=self.credentials.account_id,
        ))

if __name__ == "__main__":
    unittest.main()
