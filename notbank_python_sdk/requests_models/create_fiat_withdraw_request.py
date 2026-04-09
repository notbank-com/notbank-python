from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from notbank_python_sdk.constants import WithdrawPaymentMethod


@dataclass
class CreateFiatWithdrawRequest:
    account_id: int
    payment_method: WithdrawPaymentMethod
    currency: str
    amount: Decimal
    bank_account_id: Optional[UUID] = None
    cbu: Optional[str] = None
    person_type: Optional[str] = None
    cuit: Optional[str] = None
    name: Optional[str] = None
    user_id: Optional[UUID] = None
