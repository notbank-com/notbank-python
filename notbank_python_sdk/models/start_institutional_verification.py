from dataclasses import dataclass
from typing import Optional


@dataclass
class StartInstitutionalVerificationResponse:
    """Response of the institutional verification start endpoint.

    The server answers {"status": "success", "data": {"token": ...,
    "user_id": ...}}, so 'token' and 'user_id' are always present.

    Ticket CMKT-5996 documents the payload as {"link": ..., "user_id": ...}
    instead. The server source returns 'token' (the Sumsub access token) and
    sends the Sumsub verification url to the client by email, so this SDK
    follows the server and models 'link' as an optional field, which gets
    populated if the server ever starts returning it.
    """
    token: str
    user_id: str
    link: Optional[str] = None
