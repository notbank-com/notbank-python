from dataclasses import dataclass
from typing import Optional


@dataclass
class FiatDepositResponse:
    url: Optional[str] = None
    qr: Optional[str] = None
