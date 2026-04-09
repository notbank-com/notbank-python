from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class DepositAddressRequest:
    account_id: int
    currency: str
    network: str
    user_id: Optional[UUID] = None
