from dataclasses import dataclass
from typing import Optional


@dataclass
class StartInstitutionalVerificationResponse:
    """Response of the institutional verification start endpoint.

    The server answers {"status": "success", "data": {"link": ...,
    "user_id": ...}}.

    'link' is the Sumsub verification url the client has to be redirected to
    in order to go through the process. It is nullable: when the url cannot
    be retrieved, or there is no active applicant request for the user, the
    server still answers success with a null link and logs the problem, so
    callers must handle None.

    'user_id' is the uuid of the user the institutional process belongs to.
    """
    link: Optional[str]
    user_id: str
