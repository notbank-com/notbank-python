from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class GetProvincesRequest:
    country: str
    user_id: Optional[UUID] = None
