# Semantic Search

ContextOps supports semantic search over indexed document chunks.

## Endpoint

Endpoint: `POST /api/v1/retrieval/search`

## Request Example

```json
{
  "query": "What is the refund policy for enterprise customers?",
  "limit": 5,
  "access_level": "private"
}
```

## Response Example

```json
{
  "query": "What is the refund policy for enterprise customers?",
  "result_count": 1,
  "results": [
    {
      "chunk_id": "...",
      "document_id": "...",
      "title": "Demo Enterprise Support Policy",
      "text": "...",
      "score": 0.82,
      "chunk_index": 0,
      "source_type": "raw_text",
      "source_uri": null,
      "access_level": "private"
    }
  ]
}
```

## Current Filtering

The first retrieval filter is based on `access_level`.

## Future Improvements

- Owner-based access control
- Organization/team permissions
- Role-based document visibility
- Metadata filters
- Hybrid retrieval
- Reranking
