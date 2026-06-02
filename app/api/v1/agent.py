from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.services.agent.runtime import AgentRuntime

router = APIRouter(prefix="/agent", tags=["agent"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("/query", response_model=AgentQueryResponse)
def query_agent(
    request: AgentQueryRequest,
    db: DatabaseSession,
) -> AgentQueryResponse:
    runtime = AgentRuntime(db=db)
    return runtime.answer(request)
