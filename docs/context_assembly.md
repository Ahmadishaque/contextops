# Context Assembly

Context assembly converts raw retrieval results into a controlled context package for a future agent runtime.

## Endpoint

Endpoint: `POST /api/v1/context/assemble`

## Request Example

```json
{
  "query": "What should enterprise customers do for refund requests?",
  "limit": 5,
  "access_level": "private",
  "max_context_chars": 4000
}
```

## Response Structure

The endpoint returns a `context_package` containing:

- original query
- formatted context text
- source metadata
- source count
- total context character count
- truncation flag

## Why This Matters

Production AI agents need controlled context assembly instead of blindly passing raw retrieval results to an LLM.

This service is responsible for deciding what evidence enters the model context, how it is formatted, and whether the context budget has been exceeded.
