from fastapi import APIRouter

from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.services.agent.runtime import AgentRuntime

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/query", response_model=AgentQueryResponse)
def query_agent(request: AgentQueryRequest) -> AgentQueryResponse:
    runtime = AgentRuntime()
    return runtime.answer(request)
