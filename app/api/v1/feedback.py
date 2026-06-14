from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.feedback import FeedbackCreateRequest, FeedbackResponse
from app.services.feedback.exceptions import (
    FeedbackNotFoundError,
    TraceNotFoundError,
    TraceOwnershipError,
)
from app.services.feedback.service import FeedbackService

router = APIRouter(prefix="/feedback", tags=["feedback"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(
    request: FeedbackCreateRequest,
    db: DatabaseSession,
) -> FeedbackResponse:
    service = FeedbackService(db=db)

    try:
        feedback = service.create_feedback(request)
    except TraceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except TraceOwnershipError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    return FeedbackResponse.model_validate(feedback)


@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(
    feedback_id: str,
    db: DatabaseSession,
) -> FeedbackResponse:
    service = FeedbackService(db=db)

    try:
        feedback = service.get_feedback(feedback_id)
    except FeedbackNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return FeedbackResponse.model_validate(feedback)
