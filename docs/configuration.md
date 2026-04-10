# Configuration

This document covers all configuration options for both the backend and frontend.

## Environment Variables

### Backend (`backend/.env`)

| Variable       | Required | Default | Description                                |
| -------------- | -------- | ------- | ------------------------------------------ |
| `GROQ_API_KEY` | **yes**  | —       | API key for Groq LLM service. The backend will fail to start without it (`RuntimeError`). |

Create the file from the template:

```bash
cd backend
cp .env.example .env
# Edit .env and set GROQ_API_KEY=your_key_here
```

Environment variables are loaded by `python-dotenv` in `backend/app/utils/config.py`.

## Backend Config Constants

Defined in `backend/app/utils/config.py`:

| Constant   | Value         | Description              | Status  |
| ---------- | ------------- | ------------------------ | ------- |
| `API_HOST` | `127.0.0.1`  | Intended bind address    | Unused  |
| `API_PORT` | `8000`        | Intended bind port       | Unused  |

> **Note:** `API_HOST` and `API_PORT` are defined in `config.py` but not referenced by `main.py` or anywhere else in the application. The actual host and port are controlled entirely by uvicorn CLI arguments:
>
> ```bash
> uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
> ```

## CORS Settings

Configured in `backend/app/main.py` via `CORSMiddleware`:

| Setting              | Value                                                    |
| -------------------- | -------------------------------------------------------- |
| `allow_origins`      | `["http://localhost:3000", "http://127.0.0.1:3000"]`     |
| `allow_credentials`  | `true`                                                   |
| `allow_methods`      | `["*"]` (all HTTP methods)                               |
| `allow_headers`      | `["*"]` (all headers)                                    |

To allow additional origins (e.g., a deployed frontend), add them to the `origins` list in `main.py`.

## Groq LLM Settings

Configured in `backend/app/services/llm_service.py`:

| Setting        | Value                                             |
| -------------- | ------------------------------------------------- |
| API endpoint   | `https://api.groq.com/openai/v1/chat/completions` |
| Model          | `llama-3.1-8b-instant`                            |
| Max tokens     | `512`                                             |
| Temperature    | `0.7`                                             |
| HTTP timeout   | `30` seconds                                      |

These values are hardcoded in the service. To change the model or parameters, edit `llm_service.py` directly.

## Port Assignments

| Service  | Default Port | URL                        |
| -------- | ------------ | -------------------------- |
| Backend  | 8000         | `http://localhost:8000`    |
| Frontend | 3000         | `http://localhost:3000`    |

> **Port mismatch:** The Chat component targets port `8001` instead of `8000`. See [Getting Started — Known issue](getting-started.md#frontend-setup) for details.

## Frontend Build Configuration

### Next.js (`frontend/next.config.js`)

Default configuration — no customizations.

### TypeScript (`frontend/tsconfig.json`)

| Option                           | Value        |
| -------------------------------- | ------------ |
| `target`                         | ES2020       |
| `strict`                         | true         |
| `module`                         | ESNext       |
| `moduleResolution`               | node         |
| `jsx`                            | preserve     |
| `sourceMap`                      | true         |
| `incremental`                    | true         |
| `forceConsistentCasingInFileNames` | true       |

**Path alias:** `@/*` resolves to `src/*`.

### Tailwind CSS (`frontend/tailwind.config.js`)

- Content paths: `./src/**/*.{js,ts,jsx,tsx}`
- Theme: default (no extensions)
- Plugins: none

### PostCSS (`frontend/postcss.config.js`)

- Plugins: `tailwindcss`, `autoprefixer`

## See Also

- [Getting Started](getting-started.md) — Setup instructions
- [Backend Guide](backend.md) — Service-level configuration details
- [Frontend Guide](frontend.md) — Build tooling details
