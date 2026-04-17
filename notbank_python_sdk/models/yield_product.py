from dataclasses import dataclass
from decimal import Decimal

from notbank_python_sdk.constants import YieldTypeStr


@dataclass
class YieldProduct:
    product_title: str
    product_id: int
    description: str
    min_yield_time: int
    withdraw_delay: int
    type: YieldTypeStr
    last_change: Decimal
