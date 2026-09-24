from dataclasses import dataclass
from typing import Optional


@dataclass
class StartInstitutionalVerificationRequest:
    """Request of the institutional verification start endpoint.

    'phone' is optional and is currently ignored by the server: it is
    accepted by the payload serializer, but the phone actually used is the
    one registered for the authenticated user. It is kept to mirror the
    other Notbank SDKs.
    """
    phone: Optional[str] = None
