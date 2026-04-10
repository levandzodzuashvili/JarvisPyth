# Python Jarvis Documentation

Python Jarvis is an AI-powered chatbot application for document analysis and intelligent Q&A. It pairs a **FastAPI** backend (with Groq LLM integration and BM25 document search) with a **Next.js** TypeScript frontend.

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
