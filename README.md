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
