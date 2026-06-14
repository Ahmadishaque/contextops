from secrets import compare_digest
from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

API_KEY_HEADER_NAME = "X-API-Key"

api_key_header = APIKeyHeader(
    name=API_KEY_HEADER_NAME,
    scheme_name="ContextOps API Key",
    description="API key required to access protected ContextOps endpoints.",
    auto_error=False,
)

ProvidedAPIKey = Annotated[str | None, Security(api_key_header)]


def require_api_key(provided_api_key: ProvidedAPIKey) -> str:
    expected_api_key = settings.contextops_api_key.get_secret_value()

    if not provided_api_key or not compare_digest(
        provided_api_key,
        expected_api_key,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return provided_api_key
