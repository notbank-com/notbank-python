from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ExecuteQuoteRequest:
    quote_id: UUID
    user_id: Optional[UUID] = None


@dataclass
class ExecuteQuoteRequestInternal:
    user_id: Optional[UUID] = None


