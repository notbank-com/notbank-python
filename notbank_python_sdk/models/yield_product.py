from dataclasses import dataclass
from decimal import Decimal

from notbank_python_sdk.constants import YieldType


@dataclass
class YieldProduct:
    product_title: str
    product_id: int
    description: str
    min_yield_time: int
    type: YieldType
    last_change: Decimal
