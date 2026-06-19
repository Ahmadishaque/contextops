from dataclasses import dataclass
from time import perf_counter
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

import requests

from frontend.services import endpoints


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
        timeout_seconds: float = 30.0,
    ) -> None:
        normalized_base_url = base_url.strip().rstrip("/")
        parsed_url = urlparse(normalized_base_url)

        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ContextOpsAPIError(
                "Invalid API base URL. Use a complete URL such as "
                "http://127.0.0.1:8000"
            )

        self.base_url = normalized_base_url
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    def get_health(self) -> APIResponse:
        return self._request(
            method="GET",
            path=endpoints.HEALTH,
            authenticated=False,
        )

    def ingest_document(
        self,
        payload: dict[str, Any],
    ) -> APIResponse:
        return self._request(
            method="POST",
            path=endpoints.DOCUMENT_INGESTION,
            json_body=payload,
        )

    def search_documents(
        self,
        payload: dict[str, Any],
    ) -> APIResponse:
        return self._request(
            method="POST",
            path=endpoints.SEMANTIC_SEARCH,
            json_body=payload,
        )

    def assemble_context(
        self,
        payload: dict[str, Any],
    ) -> APIResponse:
        return self._request(
            method="POST",
            path=endpoints.CONTEXT_ASSEMBLY,
            json_body=payload,
        )

    def _request(
        self,
        *,
        method: str,
        path: str,
        authenticated: bool = True,
        json_body: dict[str, Any] | None = None,
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
                json=json_body,
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise ContextOpsAPIError(
                f"Could not connect to ContextOps API: {exc}"
            ) from exc

        latency_ms = round(
            (perf_counter() - started_at) * 1000,
            2,
        )

        try:
            response_body: Any = response.json()
        except ValueError:
            response_body = response.text

        response_request_id = response.headers.get(
            "X-Request-ID",
            request_id,
        )

        if not response.ok:
            detail = self._extract_error_detail(response_body)

            raise ContextOpsAPIError(
                f"HTTP {response.status_code}: {detail}",
                status_code=response.status_code,
                response_body=response_body,
            )

        return APIResponse(
            data=response_body,
            status_code=response.status_code,
            latency_ms=latency_ms,
            request_id=response_request_id,
        )

    @staticmethod
    def _extract_error_detail(response_body: Any) -> str:
        if isinstance(response_body, dict):
            detail = response_body.get("detail")

            if detail is not None:
                return str(detail)

        if isinstance(response_body, str) and response_body:
            return response_body

        return "Unexpected API error"
