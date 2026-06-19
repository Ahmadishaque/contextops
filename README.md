# ContextOps

Production context engineering platform for tool-using AI agents.

## Overview

ContextOps is a production-style AI engineering project focused on building the infrastructure around reliable AI agents. The system is designed to support permission-aware context assembly, retrieval, tool orchestration, tracing, evaluation, feedback loops, and production observability.

## Project Goals

- Build a production-grade backend for AI agent context management.
- Support document ingestion, retrieval, and context assembly.
- Add tool-use support through a modular tool registry.
- Track agent execution through structured traces.
- Evaluate responses for grounding, citation quality, and reliability.
- Demonstrate production AI engineering practices beyond notebook-based model development.

## Initial Tech Stack

- Python
- FastAPI
- PostgreSQL
- Qdrant
- Redis
- SQLAlchemy
- Alembic
- Pytest
- Ruff
- Mypy
- Docker
- GitHub Actions

## Development Status

Current milestone: project scaffold.

## Local Infrastructure

Start local infrastructure services:

## Continuous Integration

This project uses GitHub Actions to validate code quality on pull requests and pushes to `main`.

CI checks include:

- Ruff linting
- Pytest unit tests

Workflow file:

```text
.github/workflows/ci.yml


## Continuous Integration

This project uses GitHub Actions to validate code quality on pull requests and pushes to `main`.

CI checks include:

- Ruff linting
- Pytest unit tests

Workflow file: `.github/workflows/ci.yml`

## Production Capabilities

- FastAPI service with versioned endpoints
- PostgreSQL metadata persistence with Alembic migrations
- Qdrant semantic vector retrieval
- Redis infrastructure integration
- document ingestion and chunk indexing
- permission-filtered retrieval
- bounded context assembly
- provider-based agent runtime
- execution tracing
- deterministic response evaluation
- registered agent tools
- API-key authentication
- structured request logging and request IDs
- user feedback capture
- Docker-based deployment
- GitHub Actions lint and test pipeline

## Run with Docker

Create a local `.env` file from `.env.example`, then run:

`docker compose -f docker-compose.yml -f docker-compose.app.yml up --build -d`

Open the API documentation at `http://127.0.0.1:8000/docs`.

View API logs with:

`docker compose -f docker-compose.yml -f docker-compose.app.yml logs -f api`

Stop the stack with:

`docker compose -f docker-compose.yml -f docker-compose.app.yml down`

## Documentation

- [Architecture](docs/architecture.md)
- [Deployment](docs/deployment.md)
- [End-to-End Demo](docs/demo.md)
- [Security](docs/security.md)
- [Observability](docs/observability.md)
- [Feedback](docs/feedback.md)
- [Continuous Integration](docs/ci.md)

## Current Scope

ContextOps is a production-style portfolio implementation. It demonstrates the architecture and operational concerns of a context engineering platform while keeping local infrastructure and model usage affordable.

Future work includes autonomous tool planning, hybrid retrieval, reranking, multi-tenant authorization, distributed tracing, and asynchronous ingestion.
