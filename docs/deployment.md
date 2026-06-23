# Deployment

ContextOps can run locally as a Python application or as a containerized service.

## Container Architecture

- ContextOps API
- PostgreSQL metadata database
- Qdrant vector database
- Redis cache and coordination service

## Environment Configuration

Copy `.env.example` to `.env` and configure the required values.

At minimum, configure:

- `CONTEXTOPS_API_KEY`
- `DATABASE_URL`
- `QDRANT_URL`
- `REDIS_URL`
- `LLM_PROVIDER`
- `OPENAI_API_KEY` when the OpenAI provider is enabled

Never commit `.env`.

## Build and Run

Run the infrastructure and API together:

`docker compose -f docker-compose.yml -f docker-compose.app.yml up --build -d`

## View Logs

`docker compose -f docker-compose.yml -f docker-compose.app.yml logs -f api`

## Stop the Stack

`docker compose -f docker-compose.yml -f docker-compose.app.yml down`

## Database Migrations

The API container runs `python -m alembic upgrade head` before starting the server.

The startup process retries migrations while PostgreSQL is becoming available.

## Health Check

The container health check calls:

`GET /api/v1/health`

## Security

Application endpoints require the configured `X-API-Key` header.

The health endpoint remains public for container and orchestration health checks.

## Production Considerations

- Store secrets in a managed secret store.
- Use TLS at the ingress or load-balancer layer.
- Use managed PostgreSQL, Redis, and vector database services where appropriate.
- Configure centralized logs and metrics.
- Add resource limits and autoscaling.
- Run vulnerability and dependency scans.
- Rotate API keys regularly.
- Replace shared API keys with scoped service identities for multi-tenant deployments.
