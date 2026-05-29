# Vector Indexing

ContextOps indexes document chunks into Qdrant during ingestion.

## Flow

1. User submits raw document text.
2. The ingestion pipeline creates a document metadata row in PostgreSQL.
3. The text is split into chunks.
4. Chunks are stored in PostgreSQL.
5. Chunk text is embedded using Sentence Transformers.
6. Embeddings and metadata payloads are upserted into Qdrant.
7. Qdrant point IDs are saved back to PostgreSQL.

## Default Embedding Model

Model: `sentence-transformers/all-MiniLM-L6-v2`

Default embedding dimension: `384`

## Qdrant Collection

Collection name: `contextops_chunks`

## Why PostgreSQL + Qdrant?

PostgreSQL stores durable metadata and relational state. Qdrant stores vectors and retrieval payloads for semantic search.
