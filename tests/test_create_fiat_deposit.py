from decimal import Decimal
import unittest
from uuid import UUID
from notbank_python_sdk.constants import DepositPaymentMethod
from notbank_python_sdk.models.fiat_deposit_response import FiatDepositResponse
from notbank_python_sdk.requests_models import CreateFiatDepositRequest

from tests import test_helper

from notbank_python_sdk.notbank_client import NotbankClient

BR_BANK_ACCOUNT_ID = UUID("2ddc273f-c6af-40c1-a69a-dea1062dedcc")

CL_BANK_ACCOUNT_ID = UUID("4c0aba9d-41bd-49db-91f8-7e27dad6869e")

CO_BANK_ACCOUNT_ID = UUID("75c1839d-3c16-4466-846f-8a5df7a975c0")

PE_BANK_ACCOUNT_ID = UUID("9100427c-95f0-43db-981e-702c7bd9605b")

class TestCreateFiatDeposit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)

    def _deposit(self, payment_method, currency, amount, **kwargs):
        return self.client.create_fiat_deposit(CreateFiatDepositRequest(
            account_id=self.credentials.account_id,
            payment_method=payment_method,
            currency=currency,
            amount=amount,
            **kwargs
        ))

    # payment_method 1 (BANK_TRANSFER) + BRL, CLP → None response
    def test_bank_transfer_brl(self):
        result = self._deposit(
            DepositPaymentMethod.BANK_TRANSFER, "BRL", bank_account_id=BR_BANK_ACCOUNT_ID, amount=Decimal("1000"))
        self.assertIsNone(result)

    def test_bank_transfer_clp(self):
        result = self._deposit(
            DepositPaymentMethod.BANK_TRANSFER, "CLP", bank_account_id=CL_BANK_ACCOUNT_ID, amount=Decimal("1000"))
        self.assertIsNone(result)

    # payment_method 1 (BANK_TRANSFER) + COP → FiatDepositResponse with url
    def test_bank_transfer_cop(self):
        result = self._deposit(
            DepositPaymentMethod.BANK_TRANSFER, "COP", bank_account_id=CO_BANK_ACCOUNT_ID, amount=Decimal("4000"))
        self.assertIsInstance(result, FiatDepositResponse)
        self.assertIsNotNone(result.url)
        self.assertIsNone(result.qr)

    # payment_method 3 (VIRTUAL_WALLET) → None response
    def test_virtual_wallet(self):
        result = self._deposit(
            DepositPaymentMethod.VIRTUAL_WALLET, "PEN", bank_account_id=PE_BANK_ACCOUNT_ID, amount=Decimal("2000"))
        self.assertIsNone(result)

    # payment_method 4 (QR_CODE) → FiatDepositResponse with qr 
    def test_qr_code(self):
        result = self._deposit(DepositPaymentMethod.QR_CODE, "PEN", amount=Decimal("2000"))
        self.assertIsInstance(result, FiatDepositResponse)
        self.assertIsNotNone(result.qr)
        self.assertIsNone(result.url)

    # payment_method 5 (ASSISTED_BANK_TRANSFER) → FiatDepositResponse with url
    def test_assisted_bank_transfer(self):
        result = self._deposit(DepositPaymentMethod.ASSISTED_BANK_TRANSFER, "CLP", amount=Decimal("1000"))
        self.assertIsInstance(result, FiatDepositResponse)
        self.assertIsNotNone(result.url)
        self.assertIsNone(result.qr)

    # payment_method 6 (CREDIT_OR_DEBIT_CARD) → FiatDepositResponse with url
    def test_credit_or_debit_card(self):
        result = self._deposit(DepositPaymentMethod.CREDIT_OR_DEBIT_CARD, "CLP", amount=Decimal("1000"))
        self.assertIsInstance(result, FiatDepositResponse)
        self.assertIsNotNone(result.url)
        self.assertIsNone(result.qr)

    # payment_method 7 (CASH_OR_CARD) → FiatDepositResponse with url
    def test_cash_or_card(self):
        result = self._deposit(DepositPaymentMethod.CASH_OR_CARD, "CLP", amount=Decimal("1000"))
        self.assertIsInstance(result, FiatDepositResponse)
        self.assertIsNotNone(result.url)
        self.assertIsNone(result.qr)


if __name__ == "__main__":
    unittest.main()
