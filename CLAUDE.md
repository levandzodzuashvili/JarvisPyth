# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python Jarvis is an AI-powered chatbot for document analysis and Q&A. It has a FastAPI backend (Groq LLM + BM25 document search) and a Next.js TypeScript frontend.

## Commands

### Backend (run from `backend/`)

```bash
# Install dependencies (use a virtualenv)
pip install -r requirements-dev.txt

# Run dev server (port 8000)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Environment setup
cp .env.example .env   # then set GROQ_API_KEY

# Test
pytest
```

### Frontend (run from `frontend/`)

```bash
npm install
cp .env.example .env.local
npm run dev       # Dev server (port 3000)
npm run build     # Production build
npm run lint      # Next.js linting
npm run test:ci   # Jest
```

Set `NEXT_PUBLIC_API_BASE_URL` in `frontend/.env.local`, for example `http://127.0.0.1:8000`.

## Architecture

**Backend** (`backend/app/`): FastAPI app structured as:
- `main.py` — App factory, lifespan setup, CORS middleware, exception handlers
- `api/routes.py` — Endpoints read shared services from `request.app.state`
- `services/llm_service.py` — Calls Groq using a shared `httpx.Client` and raises typed exceptions
- `services/document_service.py` — BM25 search over in-memory sample documents seeded at startup
- `exceptions.py` — Typed chat service exceptions mapped to HTTP responses
- `models/schemas.py` — Pydantic request/response models
- `utils/config.py` — Lazy `GROQ_API_KEY` accessor

**Frontend** (`frontend/src/`): Next.js Pages Router with a single page:
- `pages/index.tsx` — Renders the Chat component
- `components/Chat.tsx` — Container component that checks config, manages state, and delegates rendering
- `components/Composer.tsx` and `components/MessageList.tsx` — Presentational UI
- `lib/config.ts` — Reads `NEXT_PUBLIC_API_BASE_URL`
- `lib/api.ts` — Owns the chat fetch boundary and typed frontend errors
- Uses Tailwind CSS for styling; TypeScript strict mode with `@/*` path alias mapping to `src/*`

**Request flow**: User types in `Chat.tsx` -> `sendChatMessage()` calls backend `/chat` -> backend calls Groq -> app-level exception handlers map failures -> frontend renders success or a generic error state.

## Key Configuration

- Backend reads `GROQ_API_KEY` lazily; missing keys only break `/chat`
- CORS is configured for `localhost:3000` and `127.0.0.1:3000` only
- Frontend requires `NEXT_PUBLIC_API_BASE_URL`
