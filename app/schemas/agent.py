from pydantic import BaseModel, Field

from app.schemas.context import ContextSource


class AgentQueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)
    access_level: str = Field(default="private", max_length=50)
    max_context_chars: int = Field(default=4000, ge=500, le=20000)


class AgentQueryResponse(BaseModel):
    query: str
    answer: str
    grounded: bool
    source_count: int
    sources: list[ContextSource]
