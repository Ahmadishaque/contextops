from pydantic import BaseModel, Field


class RetrievalSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)
    access_level: str = Field(default="private", max_length=50)


class RetrievalSearchResult(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    text: str
    score: float
    chunk_index: int
    source_type: str
    source_uri: str | None = None
    access_level: str


class RetrievalSearchResponse(BaseModel):
    query: str
    result_count: int
    results: list[RetrievalSearchResult]
