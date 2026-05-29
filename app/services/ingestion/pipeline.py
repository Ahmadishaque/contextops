from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.db.models.document import Document
from app.db.models.user import User
from app.schemas.document import DocumentIngestRequest
from app.services.ingestion.chunker import SimpleTextChunker
from app.services.retrieval.embedder import get_embedder
from app.services.retrieval.vector_store import get_vector_store


class DocumentIngestionPipeline:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.chunker = SimpleTextChunker()
        self.embedder = get_embedder()
        self.vector_store = get_vector_store()

    def ingest(self, request: DocumentIngestRequest) -> tuple[Document, int, int]:
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

        text_chunks = self.chunker.chunk(request.text)
        db_chunks: list[Chunk] = []

        for text_chunk in text_chunks:
            db_chunk = Chunk(
                document_id=document.id,
                chunk_index=text_chunk.chunk_index,
                text=text_chunk.text,
            )
            self.db.add(db_chunk)
            db_chunks.append(db_chunk)

        self.db.flush()

        indexed_chunk_count = self._index_chunks(
            document=document,
            chunks=db_chunks,
            owner=owner,
        )

        self.db.commit()
        self.db.refresh(document)

        return document, len(db_chunks), indexed_chunk_count

    def _get_or_create_user(self, email: str) -> User:
        existing_user = self.db.query(User).filter(User.email == email).one_or_none()

        if existing_user is not None:
            return existing_user

        user = User(email=email, role="user")
        self.db.add(user)
        self.db.flush()

        return user

    def _index_chunks(
        self,
        document: Document,
        chunks: list[Chunk],
        owner: User,
    ) -> int:
        if not chunks:
            return 0

        self.vector_store.ensure_collection()

        texts = [chunk.text for chunk in chunks]
        vectors = self.embedder.embed_texts(texts)

        point_ids = [str(uuid4()) for _ in chunks]
        payloads = [
            {
                "document_id": document.id,
                "chunk_id": chunk.id,
                "chunk_index": chunk.chunk_index,
                "title": document.title,
                "source_type": document.source_type,
                "source_uri": document.source_uri,
                "access_level": document.access_level,
                "owner_id": owner.id,
                "owner_email": owner.email,
                "text": chunk.text,
            }
            for chunk in chunks
        ]

        self.vector_store.upsert_chunks(
            point_ids=point_ids,
            vectors=vectors,
            payloads=payloads,
        )

        for chunk, point_id in zip(chunks, point_ids, strict=True):
            chunk.qdrant_point_id = point_id

        return len(chunks)
