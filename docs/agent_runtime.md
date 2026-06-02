# Agent Runtime

The agent runtime is responsible for producing a grounded response from an assembled context package.

## Endpoint

Endpoint: `POST /api/v1/agent/query`

## Request Example

```json
{
  "query": "What should enterprise customers provide for refund requests?",
  "limit": 5,
  "access_level": "private",
  "max_context_chars": 4000
}
```

## Response Structure

The endpoint returns:

- original query
- grounded answer
- grounded flag
- source count
- source metadata

## Current Behavior

This initial version uses a deterministic grounded responder. It does not call an external LLM yet.

The responder only uses assembled context returned by the retrieval and context assembly pipeline.

## Future Improvements

- LLM provider abstraction
- Prompt templates
- Tool registry integration
- Structured trace logging
- Citation formatting
- Hallucination checks
- Evaluation gates
