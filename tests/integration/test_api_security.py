from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_is_public() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_protected_endpoint_rejects_missing_api_key() -> None:
    response = client.get("/api/v1/tools")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key"


def test_protected_endpoint_rejects_invalid_api_key() -> None:
    response = client.get(
        "/api/v1/tools",
        headers={"X-API-Key": "incorrect-key"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key"
