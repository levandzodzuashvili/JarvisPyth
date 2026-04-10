# Contributing

Guidelines for contributing to Python Jarvis.

## Development Workflow

1. **Run both servers** during development:
   ```bash
   # Terminal 1 — Backend
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload

   # Terminal 2 — Frontend
   cd frontend
   npm run dev
   ```

2. **Make changes** — both servers support hot reload.

3. **Lint the frontend** before committing:
   ```bash
   cd frontend
   npm run lint
   ```

4. **Run the automated checks** before committing:
   ```bash
   cd backend && pytest
   cd frontend && npm run test:ci
   ```

5. **Do a quick manual pass**:
   - Check `curl http://127.0.0.1:8000/health`
   - Verify the frontend is pointed at the correct `NEXT_PUBLIC_API_BASE_URL`
   - Exercise chat from the browser with and without a configured `GROQ_API_KEY`

## Code Style

### Backend (Python)

- **Type hints** on all function signatures
- **Pydantic models** for all request/response data
- **Synchronous handlers** — existing endpoints use `def`, not `async def`
- Follow existing patterns in `app/services/` and `app/api/routes.py`
- Use `httpx` for external HTTP calls (not `requests`)
- No Python linter is currently configured (no ruff, black, or flake8)

### Frontend (TypeScript)

- **TypeScript strict mode** is enabled — no `any` types
- **Tailwind CSS** for styling — no inline styles or CSS modules
- This project uses **Pages Router** — `"use client"` is usually unnecessary here
- **Path alias** `@/` for imports from `src/`

## Adding New Features

- **Backend:** Schema → Service → Route, with shared long-lived services registered in FastAPI lifespan and accessed via `request.app.state`.
- **Frontend:** Keep transport in `src/lib/`, keep `Chat.tsx` as the orchestrator, and move presentation into focused components when UI grows.

## Conventions

- **Commits:** Use clear, descriptive commit messages
- **Branches:** Create feature branches off `main`
- **No secrets:** Never commit `.env` files or API keys — they are in `.gitignore`
- **Documentation:** Update `docs/` when adding endpoints or changing architecture

## See Also

- [Getting Started](getting-started.md) — Initial setup
- [Backend Guide](backend.md) — Backend architecture and extension patterns
- [Frontend Guide](frontend.md) — Frontend architecture and extension patterns
