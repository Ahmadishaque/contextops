# Continuous Integration

ContextOps uses GitHub Actions for continuous integration.

## Workflow

Workflow file: `.github/workflows/ci.yml`

## Triggers

- Pull requests targeting `main`
- Pushes to `main`

## Checks

- Install Python dependencies
- Run Ruff linting
- Run Pytest unit tests

## Why This Matters

CI ensures that every change is automatically validated before it is merged into the stable branch.

This supports a production-style development workflow with repeatable quality checks.
