from pydantic import BaseModel, Field


class DocumentIngestRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    text: str = Field(..., min_length=1)
    source_type: str = Field(default="raw_text", max_length=50)
    source_uri: str | None = None
    access_level: str = Field(default="private", max_length=50)
    owner_email: str = Field(default="demo@contextops.dev", max_length=255)


class DocumentIngestResponse(BaseModel):
    document_id: str
    title: str
    chunk_count: int
    indexed_chunk_count: int
    status: str
