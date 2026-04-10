# Getting Started

This guide sets up the current stabilization baseline: FastAPI on the backend, Next.js on the frontend, typed API errors, and automated tests for both sides.

## Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- Groq API key for `/chat`

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

Add `GROQ_API_KEY` to `backend/.env` if you want chat enabled.

Run the API:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify the backend:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"office"}'
```

`/health` and `/search` work without a Groq key. `/chat` returns `500` with `{"detail":"Chat service is unavailable"}` until the key is configured.

## Frontend Setup

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
```

Set `NEXT_PUBLIC_API_BASE_URL` in `frontend/.env.local`, for example:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

The frontend reads `NEXT_PUBLIC_API_BASE_URL` when the Next.js dev server starts. Restart `npm run dev` after changing `.env.local`.

## Run the Test Suite

```bash
cd backend && pytest
cd frontend && npm run lint
cd frontend && npm run test:ci
```

## Next Steps

- [Architecture](architecture.md) explains the app factory, lifespan wiring, and request flow.
- [API Reference](api-reference.md) documents status codes and payloads.
- [Configuration](configuration.md) lists backend and frontend environment settings.
