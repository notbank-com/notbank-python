
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass
class TransferFundsRequest:
    sender_account_id: int
    receiver_account_id: int
    currency_name: str
    amount: Decimal
    otp: Optional[str] = None
    notes: Optional[str] = None
    user_id: Optional[UUID] = None
