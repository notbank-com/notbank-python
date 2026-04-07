from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class GetOneStepWithdrawRequest:
    account_id: int
    user_id: Optional[UUID] = None
