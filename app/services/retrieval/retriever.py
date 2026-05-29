from typing import Any

from app.schemas.retrieval import RetrievalSearchRequest, RetrievalSearchResult
from app.services.retrieval.embedder import get_embedder
from app.services.retrieval.vector_store import get_vector_store


class SemanticRetriever:
    def __init__(self) -> None:
        self.embedder = get_embedder()
        self.vector_store = get_vector_store()

    def search(self, request: RetrievalSearchRequest) -> list[RetrievalSearchResult]:
        query_vector = self.embedder.embed_query(request.query)

        scored_points = self.vector_store.search_chunks(
            query_vector=query_vector,
            limit=request.limit,
            access_level=request.access_level,
        )

        results: list[RetrievalSearchResult] = []

        for point in scored_points:
            payload: dict[str, Any] = point.payload or {}

            results.append(
                RetrievalSearchResult(
                    chunk_id=str(payload.get("chunk_id", "")),
                    document_id=str(payload.get("document_id", "")),
                    title=str(payload.get("title", "")),
                    text=str(payload.get("text", "")),
                    score=float(point.score),
                    chunk_index=int(payload.get("chunk_index", 0)),
                    source_type=str(payload.get("source_type", "")),
                    source_uri=payload.get("source_uri"),
                    access_level=str(payload.get("access_level", "")),
                )
            )

        return results
