# Configuration

This project now uses explicit environment configuration on both sides of the stack. Backend settings are loaded lazily; frontend settings are read when the Next.js server or build starts.

## Backend Environment

Create `backend/.env` from the template:

```bash
cd backend
cp .env.example .env
```

| Variable | Required | Description |
| --- | --- | --- |
| `GROQ_API_KEY` | Only for `/chat` | Enables Groq-backed chat requests. Missing keys do not prevent the app from starting. |

If `GROQ_API_KEY` is missing:

- `GET /health` still works
- `POST /search` still works
- `POST /chat` returns `500` with `{"detail":"Chat service is unavailable"}`

## Frontend Environment

Create `frontend/.env.local` from `frontend/.env.example`:

```bash
cd frontend
cp .env.example .env.local
```

| Variable | Required | Description |
| --- | --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | Yes | Base URL for backend requests, for example `http://127.0.0.1:8000` |

This value is read when `next dev` or `next build` starts. Restart the Next.js process after changing it.

## Backend Runtime Configuration

The FastAPI app is created in `backend/app/main.py` with:

- lifespan-managed `DocumentSearchService` on `app.state.search_service`
- one shared `httpx.Client` on `app.state.http_client`
- typed exception handlers for chat service failures

The backend does not use `API_HOST` or `API_PORT` constants anymore. Host and port come from the Uvicorn command you run.

## CORS

`backend/app/main.py` allows:

- `http://localhost:3000`
- `http://127.0.0.1:3000`

Add more origins there if the frontend is served elsewhere.

## Groq Defaults

`backend/app/services/llm_service.py` currently uses:

- endpoint: `https://api.groq.com/openai/v1/chat/completions`
- model: `llama-3.1-8b-instant`
- `max_tokens`: `512`
- `temperature`: `0.7`
- timeout: `30s`

## Example Local Setup

```bash
# backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# frontend/.env.local
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```
