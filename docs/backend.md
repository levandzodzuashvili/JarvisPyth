# Backend Guide

The backend is a FastAPI application in `backend/app/`. It now uses an app factory, lifespan-managed shared services, and app-level exception handlers for chat failures.

## Project Structure

```text
backend/
├── app/
│   ├── api/routes.py
│   ├── exceptions.py
│   ├── main.py
│   ├── models/schemas.py
│   ├── services/
│   │   ├── document_service.py
│   │   └── llm_service.py
│   └── utils/config.py
├── tests/
├── requirements.txt
├── requirements-dev.txt
└── pytest.ini
```

## Application Lifecycle

- `create_app()` in `app/main.py` builds the FastAPI instance.
- Lifespan setup creates:
  - one shared `httpx.Client` on `app.state.http_client`
  - one seeded `DocumentSearchService` on `app.state.search_service`
- Lifespan shutdown closes the shared HTTP client.

## Chat Service

`app/services/llm_service.py` exposes:

- `chat_with_ai(user_message: str, client: httpx.Client) -> str`
- `create_groq_response(messages: list[dict[str, str]], client: httpx.Client, model: str = "llama-3.1-8b-instant") -> str`
- `parse_groq_response(data: dict[str, Any]) -> str`

Behavior:

- uses the shared `httpx.Client`
- pulls `GROQ_API_KEY` lazily through `get_groq_api_key()`
- raises typed exceptions instead of returning error strings

Typed exceptions live in `app/exceptions.py`:

- `ChatServiceUnavailableError`
- `GroqTimeoutError`
- `GroqUpstreamError`
- `GroqResponseFormatError`

App-level handlers in `app/main.py` translate those exceptions to the `/chat` HTTP contract.

## Search Service

`DocumentSearchService` is still a simple in-memory BM25 wrapper:

- `add_documents(docs: List[str])`
- `search(query: str, top_k: int = 5) -> List[Tuple[str, float]]`

The app seeds five sample strings during lifespan startup. Search is intentionally ephemeral in this phase.

## Adding a New Endpoint

Use the current route pattern: schema validation plus `Request` access to shared services.

```python
from fastapi import APIRouter, Request

@router.post("/my-endpoint")
def my_endpoint(req: MyRequest, request: Request):
    my_service = request.app.state.my_service
    result = my_service.do_something(req.field_name)
    return MyResponse(result=result)
```

If the endpoint needs a long-lived dependency, register it during lifespan setup in `app/main.py` and store it on `app.state`.

## Tests

Backend tests live in `backend/tests/` and run with:

```bash
cd backend
pytest
```

Coverage includes:

- `/health` and `/search` without `GROQ_API_KEY`
- `/chat` error mapping
- `top_k` validation and happy paths

## Dependencies

Runtime dependencies are in `requirements.txt`. Test dependencies are in `requirements-dev.txt`, which includes `pytest` on top of the runtime set.
