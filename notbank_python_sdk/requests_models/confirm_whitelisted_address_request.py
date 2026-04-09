from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ConfirmWhiteListedAddressRequest:
    whitelisted_address_id: UUID
    account_id: int
    sms_code: str
    user_id: Optional[UUID] = None


@dataclass
class ConfirmWhiteListedAddressRequestInternal:
    account_id: int
    sms_code: str
    user_id: Optional[UUID] = None
