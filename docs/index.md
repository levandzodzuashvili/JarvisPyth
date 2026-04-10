# Python Jarvis Documentation

Python Jarvis is a small FastAPI + Next.js chat application. The backend uses a shared lifespan-managed `httpx.Client` for Groq chat calls and a seeded in-memory BM25 index for search.

## Contents

| I want to...                        | Go to                                      |
| ----------------------------------- | ------------------------------------------ |
| Set up the project from scratch     | [Getting Started](getting-started.md)      |
| Understand the system design        | [Architecture](architecture.md)            |
| See available API endpoints         | [API Reference](api-reference.md)          |
| Work on the backend                 | [Backend Guide](backend.md)                |
| Work on the frontend                | [Frontend Guide](frontend.md)              |
| Check environment variables & ports | [Configuration](configuration.md)          |
| Contribute to the project           | [Contributing](contributing.md)            |

## Tech Stack

| Layer    | Technology                          |
| -------- | ----------------------------------- |
| Backend  | Python, FastAPI, Pydantic, httpx    |
| Frontend | TypeScript, React 18, Next.js 14   |
| Styling  | Tailwind CSS 3                      |
| LLM      | Groq API (llama-3.1-8b-instant)    |
| Search   | BM25 (rank-bm25)                   |

## Validation

- Backend tests: `cd backend && pytest`
- Frontend lint: `cd frontend && npm run lint`
- Frontend tests: `cd frontend && npm run test:ci`
