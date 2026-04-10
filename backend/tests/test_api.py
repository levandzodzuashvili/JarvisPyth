import httpx
from fastapi.testclient import TestClient

from app.main import create_app
from app.services.document_service import DocumentSearchService


def build_search_service(documents: list[str]) -> DocumentSearchService:
    service = DocumentSearchService()
    service.add_documents(documents)
    return service


def test_health_check_works_without_groq_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_works_without_groq_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with TestClient(create_app()) as client:
        response = client.post("/search", json={"query": "office"})

    assert response.status_code == 200
    assert response.json()["query"] == "office"
    assert response.json()["results"]


def test_search_defaults_top_k_to_five(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with TestClient(create_app()) as client:
        client.app.state.search_service = build_search_service(
            [
                "policy one",
                "policy two",
                "policy three",
                "policy four",
                "policy five",
                "policy six",
            ]
        )
        response = client.post("/search", json={"query": "policy"})

    assert response.status_code == 200
    assert len(response.json()["results"]) == 5


def test_search_respects_explicit_top_k(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with TestClient(create_app()) as client:
        client.app.state.search_service = build_search_service(
            [
                "policy one",
                "policy two",
                "policy three",
                "policy four",
                "policy five",
            ]
        )
        response = client.post("/search", json={"query": "policy", "top_k": 3})

    assert response.status_code == 200
    assert len(response.json()["results"]) == 3


def test_search_rejects_invalid_top_k(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    invalid_payloads = [
        {"query": "office", "top_k": None},
        {"query": "office", "top_k": 0},
        {"query": "office", "top_k": -1},
        {"query": "office", "top_k": 51},
    ]

    with TestClient(create_app()) as client:
        for payload in invalid_payloads:
            response = client.post("/search", json=payload)
            assert response.status_code == 422


def test_chat_returns_500_when_groq_key_is_missing(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with TestClient(create_app()) as client:
        response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Chat service is unavailable"}


def test_chat_returns_504_on_timeout(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    with TestClient(create_app()) as client:
        def raise_timeout(*args, **kwargs):
            raise httpx.TimeoutException("timed out")

        client.app.state.http_client.post = raise_timeout
        response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 504
    assert response.json() == {"detail": "Groq request timed out"}


def test_chat_returns_502_on_upstream_http_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    with TestClient(create_app()) as client:
        def return_upstream_error(*args, **kwargs):
            return httpx.Response(
                502,
                json={"detail": "bad gateway"},
                request=httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions"),
            )

        client.app.state.http_client.post = return_upstream_error
        response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 502
    assert response.json() == {"detail": "Groq upstream error"}


def test_chat_returns_502_on_invalid_groq_payload(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    with TestClient(create_app()) as client:
        def return_invalid_payload(*args, **kwargs):
            return httpx.Response(
                200,
                json={"unexpected": []},
                request=httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions"),
            )

        client.app.state.http_client.post = return_invalid_payload
        response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 502
    assert response.json() == {"detail": "Invalid Groq response"}
