from fastapi.testclient import TestClient

from app.core.middleware import REQUEST_ID_HEADER
from app.main import app

client = TestClient(app)


def test_response_contains_generated_request_id() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert REQUEST_ID_HEADER in response.headers
    assert response.headers[REQUEST_ID_HEADER]


def test_existing_request_id_is_propagated() -> None:
    request_id = "client-request-123"

    response = client.get(
        "/api/v1/health",
        headers={REQUEST_ID_HEADER: request_id},
    )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == request_id
