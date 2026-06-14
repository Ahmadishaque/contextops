from fastapi import APIRouter, Depends

from app.api.v1 import (
    agent,
    context,
    documents,
    evaluation,
    feedback,
    health,
    retrieval,
    tools,
    traces,
)
from app.core.security import require_api_key

api_router = APIRouter()

api_router.include_router(health.router)

protected_dependencies = [Depends(require_api_key)]

api_router.include_router(
    documents.router,
    dependencies=protected_dependencies,
)
api_router.include_router(
    retrieval.router,
    dependencies=protected_dependencies,
)
api_router.include_router(
    context.router,
    dependencies=protected_dependencies,
)
api_router.include_router(
    agent.router,
    dependencies=protected_dependencies,
)
api_router.include_router(
    traces.router,
    dependencies=protected_dependencies,
)
api_router.include_router(
    evaluation.router,
    dependencies=protected_dependencies,
)
api_router.include_router(
    tools.router,
    dependencies=protected_dependencies,
)
api_router.include_router(
    feedback.router,
    dependencies=protected_dependencies,
)
