from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import settings


class QdrantVectorStore:
    def __init__(
        self,
        url: str = settings.qdrant_url,
        collection_name: str = settings.qdrant_collection_name,
        vector_size: int = settings.embedding_dimension,
    ) -> None:
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def ensure_collection(self) -> None:
        if self.client.collection_exists(collection_name=self.collection_name):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert_chunks(
        self,
        point_ids: list[str],
        vectors: list[list[float]],
        payloads: list[dict],
    ) -> None:
        if not point_ids:
            return

        points = [
            PointStruct(
                id=point_id,
                vector=vector,
                payload=payload,
            )
            for point_id, vector, payload in zip(point_ids, vectors, payloads, strict=True)
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )


def get_vector_store() -> QdrantVectorStore:
    return QdrantVectorStore()
