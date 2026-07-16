"""
API tests for the query endpoint, driven against the stub engine.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from backend.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    # Enter the context manager so the app's lifespan runs and the engine is
    # constructed on ``app.state``.
    with TestClient(create_app()) as test_client:
        yield test_client


def test_health_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_query_returns_rich_response(client: TestClient) -> None:
    payload = {"query": "yellow spot on my paddy leaf", "language": "en"}

    response = client.post("/api/v1/query", json=payload)

    assert response.status_code == 200
    body = response.json()

    assert body["query"] == payload["query"]
    assert body["language"] == "en"
    assert isinstance(body["answer"], str) and body["answer"]
    assert body["diagnosis"]["problem"] == "Rice Blast"
    assert 0.0 <= body["diagnosis"]["confidence"] <= 1.0
    assert len(body["sources"]) >= 1
    assert body["request_id"]


def test_request_id_header_is_returned(client: TestClient) -> None:
    response = client.post("/api/v1/query", json={"query": "leaf drying from spots"})

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")
    assert response.headers["X-Request-ID"] == response.json()["request_id"]


def test_blank_query_is_rejected(client: TestClient) -> None:
    response = client.post("/api/v1/query", json={"query": "   "})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["request_id"]


def test_missing_query_is_rejected(client: TestClient) -> None:
    response = client.post("/api/v1/query", json={})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
