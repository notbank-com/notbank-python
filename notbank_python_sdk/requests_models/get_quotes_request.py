from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from notbank_python_sdk.constants import QuoteMode


@dataclass
class GetQuotesRequest:
    mode: QuoteMode
    user_id: Optional[UUID] = None
