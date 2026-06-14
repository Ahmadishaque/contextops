from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackCreateRequest(BaseModel):
    trace_id: str = Field(..., min_length=1)
    owner_email: str = Field(default="demo@contextops.dev", max_length=255)
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(default=None, max_length=2000)
    label: str | None = Field(default=None, max_length=100)


class FeedbackResponse(BaseModel):
    id: str
    user_id: str
    trace_id: str
    rating: int
    comment: str | None
    label: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
