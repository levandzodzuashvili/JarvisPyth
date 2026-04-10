# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python Jarvis is an AI-powered chatbot for document analysis and Q&A. It has a FastAPI backend (Groq LLM + BM25 document search) and a Next.js TypeScript frontend.

## Commands

### Backend (run from `backend/`)

```bash
# Install dependencies (use a virtualenv)
pip install -r requirements.txt

# Run dev server (port 8000)
uvicorn app.main:app --reload

# Environment setup
cp .env.example .env   # then set GROQ_API_KEY
```

### Frontend (run from `frontend/`)

```bash
npm install
npm run dev       # Dev server (port 3000)
npm run build     # Production build
npm run lint      # Next.js linting
```

No test framework is configured for either backend or frontend.

## Architecture

**Backend** (`backend/app/`): FastAPI app structured as:
- `main.py` — App init, CORS middleware (allows localhost:3000)
- `api/routes.py` — Three endpoints: `POST /chat`, `POST /search`, `GET /health`
- `services/llm_service.py` — Calls Groq API (model: `llama-3.1-8b-instant`) via httpx using an OpenAI-compatible endpoint
- `services/document_service.py` — BM25 search over in-memory sample documents (no persistence)
- `models/schemas.py` — Pydantic request/response models
- `utils/config.py` — Loads env vars; requires `GROQ_API_KEY`

**Frontend** (`frontend/src/`): Next.js Pages Router with a single page:
- `pages/index.tsx` — Renders the Chat component
- `components/Chat.tsx` — Client component that POSTs to `http://127.0.0.1:8001/chat` and displays messages
- Uses Tailwind CSS for styling; TypeScript strict mode with `@/*` path alias mapping to `src/*`

**Request flow**: User types in Chat.tsx -> POST to backend `/chat` -> backend calls Groq LLM API -> response streamed back to frontend.

## Key Configuration

- Backend requires `GROQ_API_KEY` env var (set in `backend/.env`)
- CORS is configured for `localhost:3000` and `127.0.0.1:3000` only
- Backend config constants are in `backend/app/utils/config.py` (API_HOST: 127.0.0.1, API_PORT: 8000)

## Known Issue

The frontend Chat component calls port 8001 (`http://127.0.0.1:8001/chat`) but the backend defaults to port 8000.
