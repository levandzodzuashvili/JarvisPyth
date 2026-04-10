# Python Jarvis

Python Jarvis is a small FastAPI + Next.js chat application. The backend sends chat prompts to Groq and exposes a BM25 search endpoint over a seeded in-memory document set.

## Project Structure

```text
JarvisPyth/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI routes
│   │   ├── exceptions.py   # Typed chat service errors
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Groq client + BM25 search
│   │   └── utils/          # Lazy configuration helpers
│   ├── tests/
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # Chat container + presentational UI
│   │   ├── lib/            # Frontend config + API helpers
│   │   ├── pages/          # Next.js Pages Router
│   │   └── styles/
│   ├── .env.example
│   └── package.json
└── docs/
```

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Add GROQ_API_KEY to enable /chat
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

`/health` and `/search` work without `GROQ_API_KEY`. `/chat` returns `500` until the key is configured.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit NEXT_PUBLIC_API_BASE_URL, e.g. http://127.0.0.1:8000
npm run dev
```

The frontend reads `NEXT_PUBLIC_API_BASE_URL` when Next.js starts the dev server or builds the client bundle. Restart `npm run dev` after changing `.env.local`.

## Commands

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run lint
cd frontend && npm run test:ci
```

## API Summary

- `POST /chat` -> `{ "response": string }` on success
- `POST /chat` -> `500`, `502`, or `504` with `{ "detail": string }` on failure
- `POST /search` -> BM25 results for seeded sample documents
- `GET /health` -> `{ "status": "ok" }`

`/search` validates `top_k` as an integer from `1` to `50`, defaulting to `5`.

## Documentation

- [Getting Started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Backend Guide](docs/backend.md)
- [Frontend Guide](docs/frontend.md)
- [Configuration](docs/configuration.md)
- [Contributing](docs/contributing.md)
