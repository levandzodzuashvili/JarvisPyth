# Repository Guidelines

## Project Structure & Module Organization
`backend/app/` contains the FastAPI server. Keep HTTP handlers in `api/routes.py`, request/response models in `models/schemas.py`, business logic in `services/`, and environment loading in `utils/config.py`. `frontend/src/` contains the Next.js app: reusable UI in `components/`, route files in `pages/`, and global styling in `styles/`. Long-form project docs live in `docs/`; update them when APIs, architecture, or setup steps change.

## Build, Test, and Development Commands
Backend setup and run:
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Frontend setup and run:
```bash
cd frontend
npm install
npm run dev
npm run build
npm run lint
```
The frontend serves on `http://localhost:3000`. The backend docs assume port `8000`, but `frontend/src/components/Chat.tsx` currently posts to `http://127.0.0.1:8001/chat`; either start Uvicorn with `--port 8001` or update the frontend URL.

## Coding Style & Naming Conventions
Use 4-space indentation in Python and keep type hints on public functions. Follow the existing FastAPI pattern: schema -> service -> route. Prefer synchronous route handlers (`def`) to match current code. In the frontend, keep TypeScript strict-safe, name React components in PascalCase (`Chat.tsx`), keep page files route-oriented and lowercase (`pages/index.tsx`), and use the `@/` alias for imports from `src/`. Styling should stay in Tailwind utility classes and `src/styles/globals.css`.

## Testing Guidelines
There is no automated test suite yet. Before opening a PR, run `npm run lint` in `frontend/` and perform manual checks: `curl http://localhost:8000/health`, verify `/docs`, and exercise chat/search through the UI or curl. If you add tests, keep backend tests under `backend/tests/` with `test_*.py` names and use descriptive frontend test names near the component they cover.

## Commit & Pull Request Guidelines
Recent commits use short, imperative summaries such as `Add comprehensive project documentation`. Keep commits focused and descriptive. PRs should include a brief summary, note any config or docs updates, list manual verification steps, and attach screenshots for UI changes in `frontend/src/`. Link the related issue when one exists.

## Security & Configuration Tips
Create `backend/.env` from `.env.example` and set `GROQ_API_KEY`; the backend raises a runtime error if it is missing. Never commit `.env` files, API keys, or other secrets.
