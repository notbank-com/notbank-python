from decimal import Decimal
from uuid import UUID

import unittest

from notbank_python_sdk.constants import WithdrawPaymentMethod
from notbank_python_sdk.requests_models import CreateFiatWithdrawRequest
from notbank_python_sdk.notbank_client import NotbankClient

from tests import test_helper

BR_BANK_ACCOUNT_ID = UUID("2ddc273f-c6af-40c1-a69a-dea1062dedcc")
CL_BANK_ACCOUNT_ID = UUID("4c0aba9d-41bd-49db-91f8-7e27dad6869e")
CO_BANK_ACCOUNT_ID = UUID("75c1839d-3c16-4466-846f-8a5df7a975c0")
PE_BANK_ACCOUNT_ID = UUID("9100427c-95f0-43db-981e-702c7bd9605b")


class TestCreateFiatWithdraw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connection = test_helper.new_rest_client_connection(
            test_helper.print_message_in, test_helper.print_message_out)
        cls.credentials = test_helper.load_credentials()
        test_helper.authenticate_connection(connection, cls.credentials)
        cls.client = NotbankClient(connection)

    def _withdraw(self, payment_method, currency, amount, **kwargs):
        return self.client.create_fiat_withdraw(CreateFiatWithdrawRequest(
            account_id=self.credentials.account_id,
            payment_method=payment_method,
            currency=currency,
            amount=amount,
            **kwargs
        ))

    # payment_method 1 + ARS → UUID withdrawal_id (requires confirmation)
    def test_bank_transfer_ars(self):
        result = self._withdraw(
            WithdrawPaymentMethod.BANK_TRANSFER, "ARS", Decimal("1000"),
            cbu="0118243162020008383701", cuit="10241600527", name="Persona")
        self.assertIsInstance(result, UUID)

    # payment_method 1 + BRL → None
    def test_bank_transfer_brl(self):
        result = self._withdraw(
            WithdrawPaymentMethod.BANK_TRANSFER, "BRL", Decimal("1000"),
            bank_account_id=BR_BANK_ACCOUNT_ID)
        self.assertIsNone(result)

    # payment_method 1 + CLP → None
    def test_bank_transfer_clp(self):
        result = self._withdraw(
            WithdrawPaymentMethod.BANK_TRANSFER, "CLP", Decimal("20000"),
            bank_account_id=CL_BANK_ACCOUNT_ID)
        self.assertIsNone(result)

    # payment_method 1 + COP → None
    def test_bank_transfer_cop(self):
        result = self._withdraw(
            WithdrawPaymentMethod.BANK_TRANSFER, "COP", Decimal("4000"),
            bank_account_id=CO_BANK_ACCOUNT_ID)
        self.assertIsNone(result)

    # payment_method 3 (VIRTUAL_WALLET) + PEN → None
    def test_virtual_wallet_pen(self):
        result = self._withdraw(
            WithdrawPaymentMethod.VIRTUAL_WALLET, "PEN", Decimal("2000"),
            bank_account_id=PE_BANK_ACCOUNT_ID)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
