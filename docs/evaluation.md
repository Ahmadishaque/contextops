# Response Evaluation

ContextOps includes a basic deterministic response evaluation layer.

## Endpoint

Endpoint: `POST /api/v1/evaluation/response`

## Current Checks

- answer is not empty
- grounded responses include sources
- ungrounded responses do not include sources
- grounded responses do not contain no-context fallback language
- answer is not suspiciously short

## Request Example

```json
{
  "query": "What should customers provide?",
  "answer": "Customers should provide account ID and invoice number.",
  "grounded": true,
  "sources": []
}
```

## Future Improvements

- faithfulness evaluation
- citation correctness checks
- retrieval relevance scoring
- LLM-as-judge evaluation
- regression test sets
- evaluation storage
- eval-gated response release

## Why This Matters

Production AI systems need automated evaluation. This first evaluator provides simple guardrails before adding more advanced scoring.
