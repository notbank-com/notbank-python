from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from notbank_python_sdk.constants import QuoteOperation


@dataclass
class CreateDirectQuoteRequest:
    account_id: int
    from_currency: str
    from_amount: Decimal
    to_currency: str
    operation: QuoteOperation
    user_id: Optional[UUID] = None
