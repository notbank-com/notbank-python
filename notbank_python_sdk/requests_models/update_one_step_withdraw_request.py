from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from notbank_python_sdk.constants import UpdateOneStepWithdrawAction


@dataclass
class UpdateOneStepWithdrawRequest:
    account_id: int
    action: UpdateOneStepWithdrawAction
    otp: str
    user_id: Optional[UUID] = None
