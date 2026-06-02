from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.trace import Trace
from app.schemas.trace import TraceResponse

router = APIRouter(prefix="/traces", tags=["traces"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("/{trace_id}", response_model=TraceResponse)
def get_trace(trace_id: str, db: DatabaseSession) -> TraceResponse:
    trace = db.query(Trace).filter(Trace.id == trace_id).one_or_none()

    if trace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trace not found",
        )

    return TraceResponse.model_validate(trace)
