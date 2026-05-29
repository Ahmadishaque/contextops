from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.db.models.document import Document
from app.db.models.user import User
from app.schemas.document import DocumentIngestRequest
from app.services.ingestion.chunker import SimpleTextChunker


class DocumentIngestionPipeline:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.chunker = SimpleTextChunker()

    def ingest(self, request: DocumentIngestRequest) -> tuple[Document, int]:
        owner = self._get_or_create_user(email=request.owner_email)

        document = Document(
            owner_id=owner.id,
            title=request.title,
            source_type=request.source_type,
            source_uri=request.source_uri,
            access_level=request.access_level,
        )

        self.db.add(document)
        self.db.flush()

        chunks = self.chunker.chunk(request.text)

        for chunk in chunks:
            db_chunk = Chunk(
                document_id=document.id,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
            )
            self.db.add(db_chunk)

        self.db.commit()
        self.db.refresh(document)

        return document, len(chunks)

    def _get_or_create_user(self, email: str) -> User:
        existing_user = self.db.query(User).filter(User.email == email).one_or_none()

        if existing_user is not None:
            return existing_user

        user = User(email=email, role="user")
        self.db.add(user)
        self.db.flush()

        return user