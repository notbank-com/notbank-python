from decimal import Decimal
import re
import unittest

from notbank_python_sdk.notbank_client import NotbankClient
from notbank_python_sdk.constants import YieldType
from notbank_python_sdk.requests_models import (
    GetYieldProductsRequest,
    DepositToYieldRequest,
    WithdrawFromYieldRequest,
)

from tests import test_helper


class TestYield(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)
        cls.products = cls.client.get_yield_products(GetYieldProductsRequest())

    def test_get_yield_products(self):
        self.assertIsNotNone(self.products)
        self.assertIsInstance(self.products, list)

    def test_deposit_to_yield(self):
        self.assertGreater(len(self.products), 0, "No yield products available to test deposit")
        product_symbol = 'USDT'
        product = next(p for p in self.products if re.search(r'\((\w+)\)', p.product_title).group(1) == product_symbol)
        response = self.client.deposit_to_yield(DepositToYieldRequest(
            account_id=self.credentials.account_id,
            amount=Decimal("100"),
            product_id=product.product_id,
            currency=product_symbol,
            type=YieldType.VARIABLE,
        ))
        self.assertIsNotNone(response)
        self.assertIsInstance(response, int)

    def test_withdraw_from_yield(self):
        self.assertGreater(len(self.products), 0, "No yield products available to test withdrawal")
        product_symbol = 'USDT'
        product = next(p for p in self.products if re.search(r'\((\w+)\)', p.product_title).group(1) == product_symbol)
        response = self.client.withdraw_from_yield(WithdrawFromYieldRequest(
            account_id=self.credentials.account_id,
            amount=Decimal("100"),
            product_id=product.product_id,
            currency=product_symbol,
            type=YieldType.VARIABLE,
        ))
        self.assertIsNotNone(response)
        self.assertIsInstance(response, int)


if __name__ == "__main__":
    unittest.main()
