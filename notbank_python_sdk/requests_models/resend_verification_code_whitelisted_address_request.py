from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ResendVerificationCodeWhitelistedAddressRequest:
    whitelisted_address_id: UUID
    account_id: int
    user_id: Optional[UUID] = None


@dataclass
class ResendVerificationCodeWhitelistedAddressInternal:
    account_id: int
    user_id: Optional[UUID] = None
