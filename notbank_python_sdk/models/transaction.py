
from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Transaction:
    id: int
    legacy_id: str
    currency: str
    direction: int
    amount: Decimal
    fee: str
    balance: Decimal
    address: str
    hash: str
    type: int
    sub_type: int
    status: int
    created_at: str
    updated_at: str


@dataclass
class Transactions:
    total: int
    data: List[Transaction]
