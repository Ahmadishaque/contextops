from pydantic import BaseModel, Field


class ContextAssembleRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)
    access_level: str = Field(default="private", max_length=50)
    max_context_chars: int = Field(default=4000, ge=500, le=20000)


class ContextSource(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    score: float
    chunk_index: int
    source_type: str
    source_uri: str | None = None
    access_level: str


class ContextPackage(BaseModel):
    query: str
    context_text: str
    sources: list[ContextSource]
    source_count: int
    total_context_chars: int
    truncated: bool


class ContextAssembleResponse(BaseModel):
    context_package: ContextPackage
