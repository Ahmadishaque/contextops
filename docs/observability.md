# Request Observability

ContextOps includes structured request logging and request ID propagation.

## Request IDs

Every HTTP request receives a unique request identifier.

Response header: `X-Request-ID`

Clients may provide their own request ID using the same header. ContextOps propagates that value in the response and logs.

## Structured Logs

Request logs are emitted as JSON and include:

- event name
- timestamp
- request ID
- HTTP method
- request path
- response status code
- latency in milliseconds
- client host

## Success Event

`request_completed`

## Failure Event

`request_failed`

## Why This Matters

Request IDs allow engineers to correlate client errors, API logs, agent traces, and downstream service activity.

Structured JSON logs are easier to query and aggregate in production logging systems.

## Future Improvements

- OpenTelemetry traces
- Prometheus metrics
- request counters
- p50, p95, and p99 latency dashboards
- distributed trace propagation
- correlation between request IDs and agent trace IDs
