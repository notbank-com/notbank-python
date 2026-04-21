from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID
from notbank_python_sdk.models.bank import Bank


@dataclass
class BankAccount:
    id: UUID
    country: str
    bank: Optional[Bank]
    number: str
    kind: str
    currency: str
    agency: Optional[str]
    dv: Optional[str]
    province: Optional[str]
    pix_type: Optional[str]


@dataclass
class BankAccounts:
    total: int
    data: List[BankAccount]
