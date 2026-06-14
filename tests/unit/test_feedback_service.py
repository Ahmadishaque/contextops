from unittest.mock import MagicMock

import pytest

from app.schemas.feedback import FeedbackCreateRequest
from app.services.feedback.exceptions import (
    FeedbackNotFoundError,
    TraceNotFoundError,
    TraceOwnershipError,
)
from app.services.feedback.service import FeedbackService


def make_request() -> FeedbackCreateRequest:
    return FeedbackCreateRequest(
        trace_id="trace_123",
        owner_email="demo@contextops.dev",
        rating=5,
        comment="The answer was accurate and useful.",
        label="helpful",
    )


def test_create_feedback_for_owned_trace() -> None:
    db = MagicMock()

    user = MagicMock()
    user.id = "user_123"

    trace = MagicMock()
    trace.id = "trace_123"
    trace.user_id = "user_123"

    db.query.return_value.filter.return_value.one_or_none.return_value = trace

    service = FeedbackService(db=db)
    service.user_resolver.get_or_create_user = MagicMock(return_value=user)

    feedback = service.create_feedback(make_request())

    assert feedback.user_id == "user_123"
    assert feedback.trace_id == "trace_123"
    assert feedback.rating == 5
    assert feedback.label == "helpful"
    db.add.assert_called()
    db.commit.assert_called()
    db.refresh.assert_called()


def test_create_feedback_rejects_missing_trace() -> None:
    db = MagicMock()

    user = MagicMock()
    user.id = "user_123"

    db.query.return_value.filter.return_value.one_or_none.return_value = None

    service = FeedbackService(db=db)
    service.user_resolver.get_or_create_user = MagicMock(return_value=user)

    with pytest.raises(TraceNotFoundError):
        service.create_feedback(make_request())


def test_create_feedback_rejects_trace_owned_by_another_user() -> None:
    db = MagicMock()

    user = MagicMock()
    user.id = "user_123"

    trace = MagicMock()
    trace.id = "trace_123"
    trace.user_id = "different_user"

    db.query.return_value.filter.return_value.one_or_none.return_value = trace

    service = FeedbackService(db=db)
    service.user_resolver.get_or_create_user = MagicMock(return_value=user)

    with pytest.raises(TraceOwnershipError):
        service.create_feedback(make_request())


def test_get_feedback_rejects_unknown_feedback_id() -> None:
    db = MagicMock()
    db.query.return_value.filter.return_value.one_or_none.return_value = None

    service = FeedbackService(db=db)

    with pytest.raises(FeedbackNotFoundError):
        service.get_feedback("missing_feedback")
