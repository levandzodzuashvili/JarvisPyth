# Architecture

This document describes the system architecture of Python Jarvis, including component responsibilities, request flows, and key design decisions.

## System Overview

Python Jarvis is a two-tier application: a Next.js frontend that communicates over HTTP with a FastAPI backend. The backend integrates with the Groq cloud API for LLM inference and provides an in-memory BM25 search engine for document retrieval.

```mermaid
graph LR
    User["Browser<br/>(localhost:3000)"]
    Frontend["Next.js<br/>Frontend"]
    Backend["FastAPI<br/>Backend<br/>(localhost:8000)"]
    Groq["Groq API<br/>(llama-3.1-8b-instant)"]
    BM25["BM25 Search<br/>(in-memory)"]
    Client["Any HTTP Client"]

    User --> Frontend
    Frontend -->|"POST /chat"| Backend
    Client -.->|"POST /search"| Backend
    Backend -->|"OpenAI-compatible<br/>REST API"| Groq
    Backend --> BM25
```

> The frontend currently only uses `POST /chat`. The `POST /search` endpoint is available but not yet integrated into the UI.

## Request Flows

### Chat Flow (`POST /chat`)

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant F as Next.js Frontend
    participant B as FastAPI Backend
    participant G as Groq API

    U->>F: Types message, clicks Send
    F->>B: POST /chat {"message": "..."}
    B->>B: Build messages array<br/>(system prompt + user message)
    B->>G: POST /openai/v1/chat/completions<br/>model: llama-3.1-8b-instant<br/>max_tokens: 512, temperature: 0.7
    G-->>B: {"choices": [{"message": {"content": "..."}}]}
    B->>B: Parse response
    B-->>F: {"response": "..."}
    F-->>U: Display assistant message
```

### Search Flow (`POST /search`)

```mermaid
sequenceDiagram
    participant C as Client
    participant B as FastAPI Backend
    participant S as BM25 Search Service

    C->>B: POST /search {"query": "...", "top_k": 5}
    B->>S: search(query, top_k)
    S->>S: Tokenize query (whitespace split)
    S->>S: Score documents with BM25Okapi
    S->>S: Filter scores > 0, sort descending
    S-->>B: [(document, score), ...]
    B-->>C: {"query": "...", "results": [{"document": "...", "score": 0.8}]}
```

## Component Responsibilities

| Component | Location | Responsibility |
| --------- | -------- | -------------- |
| **FastAPI App** | `backend/app/main.py` | App initialization, CORS middleware, router mounting |
| **API Routes** | `backend/app/api/routes.py` | Request handling for `/chat`, `/search`, `/health` |
| **LLM Service** | `backend/app/services/llm_service.py` | Groq API communication via httpx |
| **Document Service** | `backend/app/services/document_service.py` | BM25-based document indexing and search |
| **Schemas** | `backend/app/models/schemas.py` | Pydantic request/response validation |
| **Config** | `backend/app/utils/config.py` | Environment variable loading |
| **Chat UI** | `frontend/src/components/Chat.tsx` | Message display, user input, API calls |
| **Pages** | `frontend/src/pages/` | Next.js page routing (single page) |

## Design Notes

- **Groq as LLM provider** — The integration uses the OpenAI-compatible chat completions format (`/openai/v1/chat/completions`), so swapping to another OpenAI-compatible provider would require only a URL and key change.
- **BM25 for search** — `rank-bm25` (BM25Okapi) provides keyword-based ranking with no external infrastructure. Documents are tokenized via whitespace split — no stemming or NLP pipeline.
- **No database** — Documents live in-memory and reset on restart. This keeps the setup to a single dependency (Groq API key).
- **Separate frontend and backend** — FastAPI provides auto-generated OpenAPI docs and Pydantic validation. Next.js provides file-based routing and a React development experience. All current endpoints are synchronous (`def`, not `async def`).

## See Also

- [API Reference](api-reference.md) — Detailed endpoint specifications
- [Backend Guide](backend.md) — Deep dive into backend services
- [Frontend Guide](frontend.md) — Frontend component architecture
- [Configuration](configuration.md) — All configuration options
