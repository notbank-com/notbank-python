from dataclasses import dataclass
from typing import Optional


@dataclass
class GetSubaccountsRequest:
    user_id: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
