from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class GetYieldProductsRequest:
    user_id: Optional[UUID] = None
