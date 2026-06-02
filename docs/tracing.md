# Agent Tracing

ContextOps stores structured traces for agent query executions.

## What Gets Traced

- user ID
- query
- response
- status
- latency in milliseconds
- estimated prompt tokens
- estimated completion tokens
- creation timestamp

## Agent Query Response

The `/api/v1/agent/query` endpoint returns trace metadata:

```json
{
  "trace_id": "...",
  "latency_ms": 123.45
}
```

## Trace Lookup

Endpoint: `GET /api/v1/traces/{trace_id}`

## Why This Matters

Production AI systems need traceability. A trace allows engineers to inspect model behavior, latency, failures, and response quality after deployment.

Future versions will expand traces to include retrieval events, context assembly events, tool calls, provider metadata, cost, and evaluation results.
