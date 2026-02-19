from dataclasses import dataclass
from typing import List


@dataclass
class Subaccount:
    id: int
    alias: str
    created_at: str


@dataclass
class Subaccounts:
    total: int
    data: List[Subaccount]
