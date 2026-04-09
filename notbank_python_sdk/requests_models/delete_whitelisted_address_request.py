from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class DeleteWhiteListedAddressRequest:
    whitelisted_address_id: UUID
    account_id: int
    otp: str
    user_id: Optional[UUID] = None


@dataclass
class DeleteWhiteListedAddressRequestInternal:
    account_id: int
    otp: str
    user_id: Optional[UUID] = None
