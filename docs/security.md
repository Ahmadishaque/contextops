# API Security

ContextOps protects application endpoints with API-key authentication.

## Header

Protected requests must include:

`X-API-Key: <configured-api-key>`

## Configuration

Set the API key through the environment:

`CONTEXTOPS_API_KEY=replace_with_a_long_random_value`

Do not commit the local `.env` file.

## Public Endpoints

- `GET /`
- `GET /api/v1/health`
- `/docs` and `/openapi.json` during development

## Protected Endpoints

- document ingestion
- semantic retrieval
- context assembly
- agent queries
- trace access
- response evaluation
- tool discovery and execution

## Implementation Notes

- API keys are loaded through Pydantic Settings.
- The configured key is stored as `SecretStr` to reduce accidental disclosure.
- Keys are compared using constant-time comparison.
- Invalid or missing credentials return HTTP 401.

## Limitations

API-key authentication is appropriate for the current service-to-service MVP. Future production versions should add user identity, scoped credentials, key rotation, RBAC, and organization-aware authorization.
