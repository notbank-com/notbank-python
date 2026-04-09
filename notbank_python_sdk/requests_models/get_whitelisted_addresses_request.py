from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class GetWhitelistedAddressesRequest:
    account_id: int
    search: Optional[str] = None
    user_id: Optional[UUID] = None
