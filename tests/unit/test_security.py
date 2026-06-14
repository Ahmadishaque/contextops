import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.core.security import require_api_key


def test_require_api_key_accepts_valid_key() -> None:
    api_key = settings.contextops_api_key.get_secret_value()

    result = require_api_key(api_key)

    assert result == api_key


def test_require_api_key_rejects_missing_key() -> None:
    with pytest.raises(HTTPException) as error:
        require_api_key(None)

    assert error.value.status_code == 401
    assert error.value.detail == "Invalid or missing API key"


def test_require_api_key_rejects_invalid_key() -> None:
    with pytest.raises(HTTPException) as error:
        require_api_key("incorrect-key")

    assert error.value.status_code == 401
    assert error.value.detail == "Invalid or missing API key"
