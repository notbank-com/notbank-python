from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class GetClientBankAccountsRequest:
    page: Optional[int] = None
    page_size: Optional[int] = None
    user_id: Optional[UUID] = None
