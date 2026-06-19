# End-to-End Demo

## 1. Start ContextOps

`docker compose -f docker-compose.yml -f docker-compose.app.yml up --build -d`

## 2. Open the API Documentation

Open `http://127.0.0.1:8000/docs`.

## 3. Authenticate

Use the Swagger Authorize button and provide the configured ContextOps API key.

## 4. Ingest a Document

Use the document ingestion endpoint to submit text and metadata.

The ingestion pipeline:

- creates document metadata
- splits text into chunks
- stores chunk metadata in PostgreSQL
- generates embeddings
- indexes vectors in Qdrant

## 5. Search Documents

Call the semantic retrieval endpoint with a question and access level.

Review the returned chunks, similarity scores, and source metadata.

## 6. Assemble Context

Call the context endpoint to produce a bounded context package from retrieved evidence.

## 7. Query the Agent

Call the agent query endpoint.

The response includes the generated answer, source references, and execution trace ID.

## 8. Inspect the Trace

Retrieve the trace using its trace ID to inspect request and execution metadata.

## 9. Evaluate the Response

Submit the answer and evidence to the evaluation endpoint.

## 10. Submit Feedback

Submit a rating, label, and optional comment linked to the trace.

## 11. Review Observability

Run:

`docker compose -f docker-compose.yml -f docker-compose.app.yml logs -f api`

Observe structured request logs containing request IDs, status codes, paths, and latency.

## 12. Stop the Stack

`docker compose -f docker-compose.yml -f docker-compose.app.yml down`
