from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import settings


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = settings.embedding_model) -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return [embedding.tolist() for embedding in embeddings]

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]


@lru_cache(maxsize=1)
def get_embedder() -> SentenceTransformerEmbedder:
    return SentenceTransformerEmbedder()
