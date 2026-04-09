from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from notbank_python_sdk.constants import YieldType


@dataclass
class DepositToYieldRequest:
    account_id: int
    amount: Decimal
    product_id: int
    currency: str
    type: YieldType
    user_id: Optional[UUID] = None
