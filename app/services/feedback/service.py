from sqlalchemy.orm import Session

from app.db import base as _db_base  # noqa: F401
from app.db.models.feedback import Feedback
from app.db.models.trace import Trace
from app.schemas.feedback import FeedbackCreateRequest
from app.services.feedback.exceptions import (
    FeedbackNotFoundError,
    TraceNotFoundError,
    TraceOwnershipError,
)
from app.services.tracing.user_resolver import UserResolver


class FeedbackService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_resolver = UserResolver(db=db)

    def create_feedback(self, request: FeedbackCreateRequest) -> Feedback:
        user = self.user_resolver.get_or_create_user(email=request.owner_email)

        trace = (
            self.db.query(Trace)
            .filter(Trace.id == request.trace_id)
            .one_or_none()
        )

        if trace is None:
            raise TraceNotFoundError(
                f"Trace not found: {request.trace_id}"
            )

        if trace.user_id != user.id:
            raise TraceOwnershipError(
                "Feedback cannot be submitted for a trace owned by another user"
            )

        feedback = Feedback(
            user_id=user.id,
            trace_id=trace.id,
            rating=request.rating,
            comment=request.comment,
            label=request.label,
        )

        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)

        return feedback

    def get_feedback(self, feedback_id: str) -> Feedback:
        feedback = (
            self.db.query(Feedback)
            .filter(Feedback.id == feedback_id)
            .one_or_none()
        )

        if feedback is None:
            raise FeedbackNotFoundError(
                f"Feedback not found: {feedback_id}"
            )

        return feedback
