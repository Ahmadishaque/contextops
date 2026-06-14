from time import perf_counter
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.logging import get_logger
from app.core.request_context import reset_request_id, set_request_id

logger = get_logger(__name__)

REQUEST_ID_HEADER = "X-Request-ID"


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER, str(uuid4()))
        token = set_request_id(request_id)
        start_time = perf_counter()

        try:
            response = await call_next(request)

            latency_ms = round(
                (perf_counter() - start_time) * 1000,
                2,
            )

            response.headers[REQUEST_ID_HEADER] = request_id

            logger.info(
                "request_completed",
                http_method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                latency_ms=latency_ms,
                client_host=self._get_client_host(request),
            )

            return response

        except Exception:
            latency_ms = round(
                (perf_counter() - start_time) * 1000,
                2,
            )

            logger.exception(
                "request_failed",
                http_method=request.method,
                path=request.url.path,
                latency_ms=latency_ms,
                client_host=self._get_client_host(request),
            )

            raise

        finally:
            reset_request_id(token)

    @staticmethod
    def _get_client_host(request: Request) -> str | None:
        if request.client is None:
            return None

        return request.client.host
