from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.document import DocumentIngestRequest, DocumentIngestResponse
from app.services.ingestion.pipeline import DocumentIngestionPipeline

router = APIRouter(prefix="/documents", tags=["documents"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/ingest",
    response_model=DocumentIngestResponse,
    status_code=status.HTTP_201_CREATED,
)
def ingest_document(
    request: DocumentIngestRequest,
    db: DatabaseSession,
) -> DocumentIngestResponse:
    pipeline = DocumentIngestionPipeline(db=db)
    document, chunk_count, indexed_chunk_count = pipeline.ingest(request)

    return DocumentIngestResponse(
        document_id=document.id,
        title=document.title,
        chunk_count=chunk_count,
        indexed_chunk_count=indexed_chunk_count,
        status="ingested",
    )
