from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class GetClientBankAccountRequest:
    bank_account_id: UUID
    user_id: Optional[UUID] = None


@dataclass
class GetClientBankAccountRequestInternal:
    user_id: Optional[UUID] = None


