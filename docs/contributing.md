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

4. **Test manually** — no automated test suite is configured yet. Verify changes by:
   - Hitting the health check: `curl http://localhost:8000/health`
   - Testing chat through the UI or curl
   - Checking the Swagger UI at `http://localhost:8000/docs`

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
- This project uses **Pages Router** — `"use client"` is not required (see [Frontend Guide](frontend.md#adding-a-new-component))
- **Path alias** `@/` for imports from `src/`

## Adding New Features

- **Backend:** Schema → Service → Route. See [Backend Guide — Adding a New Endpoint](backend.md#adding-a-new-endpoint) for step-by-step examples.
- **Frontend:** Component → Page (if needed). See [Frontend Guide — Adding a New Component](frontend.md#adding-a-new-component) for examples.

## Conventions

- **Commits:** Use clear, descriptive commit messages
- **Branches:** Create feature branches off `main`
- **No secrets:** Never commit `.env` files or API keys — they are in `.gitignore`
- **Documentation:** Update `docs/` when adding endpoints or changing architecture

## See Also

- [Getting Started](getting-started.md) — Initial setup
- [Backend Guide](backend.md) — Backend architecture and extension patterns
- [Frontend Guide](frontend.md) — Frontend architecture and extension patterns
