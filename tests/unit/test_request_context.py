from app.core.request_context import (
    get_request_id,
    reset_request_id,
    set_request_id,
)


def test_request_id_context_can_be_set_and_reset() -> None:
    token = set_request_id("request-123")

    assert get_request_id() == "request-123"

    reset_request_id(token)

    assert get_request_id() is None
