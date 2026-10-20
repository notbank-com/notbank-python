"""Test doubles for the unit tests that check how NotbankClient builds a
request and parses its response, without a real connection."""
import json
from typing import Any, List, NamedTuple

from notbank_python_sdk.client_connection import ClientConnection, RequestType
from notbank_python_sdk.core.endpoint_category import EndpointCategory


class RecordedRequest(NamedTuple):
    request_type: RequestType
    endpoint: str
    endpoint_category: EndpointCategory
    request_data: Any


def _unexpected(name: str):
    def call(*args, **kwargs):
        raise AssertionError("unexpected call to " + name)
    return call


class StubConnection:
    """Records the request done by the client and answers with canned,
    already unwrapped, response data (the envelope unwrapping happens in the
    rest layer, below this point)."""

    def __init__(self, response_data: Any) -> None:
        self._response_data = response_data
        self.calls = []  # type: List[RecordedRequest]

    def _recorder(self, request_type: RequestType):
        def request_fn(endpoint, endpoint_category, request_data, parse_response_fn):
            self.calls.append(RecordedRequest(
                request_type, endpoint, endpoint_category, request_data))
            return parse_response_fn(self._response_data)
        return request_fn

    def as_client_connection(self) -> ClientConnection:
        return ClientConnection(
            post_request=self._recorder(RequestType.POST),
            get_request=self._recorder(RequestType.GET),
            delete_request=self._recorder(RequestType.DELETE),
            subscribe=_unexpected("subscribe"),
            unsubscribe=_unexpected("unsubscribe"),
            authenticate_user=_unexpected("authenticate_user"),
            connect=lambda: None,
            close=lambda: None,
        )

    @property
    def last_call(self) -> RecordedRequest:
        return self.calls[-1]


class FakeResponse:
    """Minimal stand in for requests.Response. The response handler only uses
    json(), status_code and text."""

    def __init__(self, payload: Any, status_code: int = 200) -> None:
        self.status_code = status_code
        self.text = json.dumps(payload)

    def json(self, **kwargs: Any) -> Any:
        return json.loads(self.text, **kwargs)
