from pydantic import BaseModel, Field

from app.schemas.context import ContextSource


class ResponseEvaluationRequest(BaseModel):
    query: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    grounded: bool
    sources: list[ContextSource]


class ResponseEvaluationResult(BaseModel):
    passed: bool
    grounded: bool
    source_count: int
    answer_length: int
    has_sources: bool
    has_empty_answer: bool
    has_no_context_fallback: bool
    warnings: list[str]


class ResponseEvaluationResponse(BaseModel):
    query: str
    evaluation: ResponseEvaluationResult
