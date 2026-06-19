from dataclasses import dataclass
from time import perf_counter
from typing import Any
from uuid import uuid4

import requests


@dataclass(frozen=True)
class APIResponse:
    data: Any
    status_code: int
    latency_ms: float
    request_id: str | None


class ContextOpsAPIError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response_body: Any = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class ContextOpsAPIClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout_seconds: float = 15.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    def get_health(self) -> APIResponse:
        return self._request(
            method="GET",
            path="/api/v1/health",
            authenticated=False,
        )

    def _request(
        self,
        *,
        method: str,
        path: str,
        authenticated: bool = True,
        json: dict[str, Any] | None = None,
    ) -> APIResponse:
        request_id = str(uuid4())

        headers = {
            "Accept": "application/json",
            "X-Request-ID": request_id,
        }

        if authenticated and self.api_key:
            headers["X-API-Key"] = self.api_key

        started_at = perf_counter()

        try:
            response = requests.request(
                method=method,
                url=f"{self.base_url}{path}",
                headers=headers,
                json=json,
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise ContextOpsAPIError(
                f"Could not connect to ContextOps API: {exc}"
            ) from exc

        latency_ms = round((perf_counter() - started_at) * 1000, 2)

        try:
            response_body: Any = response.json()
        except ValueError:
            response_body = response.text

        response_request_id = response.headers.get(
            "X-Request-ID",
            request_id,
        )

        if not response.ok:
            raise ContextOpsAPIError(
                f"ContextOps API returned HTTP {response.status_code}",
                status_code=response.status_code,
                response_body=response_body,
            )

        return APIResponse(
            data=response_body,
            status_code=response.status_code,
            latency_ms=latency_ms,
            request_id=response_request_id,
        )
