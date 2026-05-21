# Local Infrastructure

ContextOps uses Docker Compose for local development infrastructure.

## Services

| Service | Purpose | Local URL |
|---|---|---|
| PostgreSQL | Metadata database for users, documents, chunks, traces, and feedback | `localhost:5432` |
| Qdrant | Vector database for document embeddings | `http://localhost:6333` |
| Redis | Cache and future async worker backend | `localhost:6379` |

## Start Services

```bash
docker compose up -d
```
