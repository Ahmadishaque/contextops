import pytest
from pydantic import ValidationError

from app.schemas.feedback import FeedbackCreateRequest


def test_feedback_rating_accepts_valid_value() -> None:
    request = FeedbackCreateRequest(
        trace_id="trace_123",
        rating=5,
    )

    assert request.rating == 5


def test_feedback_rating_rejects_value_below_one() -> None:
    with pytest.raises(ValidationError):
        FeedbackCreateRequest(
            trace_id="trace_123",
            rating=0,
        )


def test_feedback_rating_rejects_value_above_five() -> None:
    with pytest.raises(ValidationError):
        FeedbackCreateRequest(
            trace_id="trace_123",
            rating=6,
        )
