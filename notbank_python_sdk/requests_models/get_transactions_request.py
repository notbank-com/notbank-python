from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from notbank_python_sdk.constants import WalletTransactionSubType, WalletTransactionType


@dataclass
class GetTransactionsRequest:
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    sort: Optional[str] = None
    currency: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    account_id: Optional[int] = None
    type: Optional[WalletTransactionType] = None
    sub_type: Optional[WalletTransactionSubType] = None
    user_id: Optional[UUID] = None
