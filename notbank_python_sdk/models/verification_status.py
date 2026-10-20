from dataclasses import dataclass
from enum import Enum
from typing import Optional


class VerificationLevel(str, Enum):
    BASIC = "basic"
    TRADER = "trader"
    TRADER_PLUS = "trader_plus"
    INSTITUTIONAL = "institutional"


class VerificationProcessResult(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class VerificationStatus:
    """Response of the verification status v2 endpoint.

    'locked' is True when the user cannot act on the verification right now
    (for example, the process is under review, the user is blocked, or a
    rejected business tries to verify again).

    'is_business' tells if the user is considered a business (an institution).

    'verification_tier' is the current verification tier of the user, one of
    0, 1, 2, 3 or 4.

    'id' is the id of the current pending verification process, None when
    there is none. The server answers success in that case, so callers must
    handle a None 'id'.

    'next_level' is the level the user can advance to, None when the user is
    already at the highest level.

    'last_previous_status' is the result of the previous process of the same
    level, None when there is none.

    'last_previous_reason' is the rejection code of the previous process. It
    is never None when 'last_previous_status' is rejected. The list of codes
    is open, so it is kept as a plain string.
    """
    locked: bool
    is_business: bool
    verification_tier: int
    id: Optional[str] = None
    next_level: Optional[VerificationLevel] = None
    last_previous_status: Optional[VerificationProcessResult] = None
    last_previous_reason: Optional[str] = None
