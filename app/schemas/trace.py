from datetime import datetime

from pydantic import BaseModel


class TraceResponse(BaseModel):
    id: str
    user_id: str
    query: str
    response: str | None
    status: str
    latency_ms: float | None
    prompt_tokens: int | None
    completion_tokens: int | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
