from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass
class CreateInverseQuoteRequest:
    account_id: int
    from_currency: str
    to_currency: str
    to_amount: Decimal
    user_id: Optional[UUID] = None

