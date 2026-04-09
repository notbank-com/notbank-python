from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

from notbank_python_sdk.constants import BankAccountKind, PixType


@dataclass
class AddClientBankAccountRequest:
    country: str
    bank: str
    number: str
    kind: BankAccountKind
    pix_type: Optional[PixType] = None
    agency: Optional[str] = None
    dv: Optional[str] = None
    province: Optional[str] = None
    user_id: Optional[UUID] = None
