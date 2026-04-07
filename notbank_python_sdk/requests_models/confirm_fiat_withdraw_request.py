from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ConfirmFiatWithdrawRequest:
    withdrawal_id: UUID
    attempt_code: str
    user_id: Optional[UUID] = None


@dataclass
class ConfirmFiatWithdrawRequestInternal:
    attempt_code: str
    user_id: Optional[UUID] = None
