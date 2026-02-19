from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateSubaccountRequest:
    alias: str
    user_id: Optional[str] = None
