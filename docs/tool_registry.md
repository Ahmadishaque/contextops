# Tool Registry

ContextOps includes a modular tool registry for agent-accessible tools.

## Endpoints

List tools: `GET /api/v1/tools`

Run tool: `POST /api/v1/tools/run`

## Initial Tools

- `calculator`: safely evaluates basic arithmetic expressions
- `document_search`: searches indexed document chunks using semantic retrieval

## Calculator Example

```json
{
  "tool_name": "calculator",
  "arguments": {
    "expression": "2 + 3 * 4"
  }
}
```

## Document Search Example

```json
{
  "tool_name": "document_search",
  "arguments": {
    "query": "What should enterprise customers provide for refund requests?",
    "limit": 5,
    "access_level": "private"
  }
}
```

## Design Goal

The registry decouples agent runtime logic from concrete tool implementations.

Future versions can add SQL tools, GitHub tools, ticket search tools, calendar tools, MCP adapters, and sandboxed execution tools.

## Safety Note

The calculator tool uses a restricted AST-based evaluator instead of Python eval.
