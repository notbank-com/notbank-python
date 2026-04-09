from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from notbank_python_sdk.constants import DepositPaymentMethod


@dataclass
class CreateFiatDepositRequest:
    account_id: int
    payment_method: DepositPaymentMethod
    currency: str
    amount: Decimal
    bank_account_id: Optional[UUID] = None
    voucher: Optional[str] = None
    user_id: Optional[UUID] = None
