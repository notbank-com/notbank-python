from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class DeleteClientBankAccountRequest:
    bank_account_id: UUID
    user_id: Optional[UUID] = None


@dataclass
class DeleteClientBankAccountRequestInternal:
    user_id: Optional[UUID] = None


