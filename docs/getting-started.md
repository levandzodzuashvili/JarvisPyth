# Getting Started

This guide walks you through setting up Python Jarvis for local development.

## Prerequisites

- **Python 3.9+**
- **Node.js 18+** and npm
- **Groq API key** — obtain one from [Groq Console](https://console.groq.com)

## Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your GROQ_API_KEY
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The API is now running at `http://localhost:8000`.

### Verify the backend

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

FastAPI also auto-generates interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Frontend Setup

In a separate terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend is now running at `http://localhost:3000`.

Open your browser to `http://localhost:3000` — you should see the Python Jarvis chat interface.

> **Known issue:** The Chat component currently sends requests to port `8001` (`http://127.0.0.1:8001/chat`), but the backend defaults to port `8000`. Either update `frontend/src/components/Chat.tsx` to use port `8000`, or start the backend on port `8001`:
> ```bash
> uvicorn app.main:app --reload --port 8001
> ```

## Project Structure

```
JarvisPyth/
├── backend/          # FastAPI Python application
│   ├── app/
│   │   ├── main.py           # App initialization, CORS
│   │   ├── api/routes.py     # API endpoints
│   │   ├── services/         # Business logic (LLM, search)
│   │   ├── models/schemas.py # Pydantic models
│   │   └── utils/config.py   # Configuration
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # Next.js TypeScript application
│   ├── src/
│   │   ├── components/Chat.tsx  # Main chat UI
│   │   ├── pages/               # Next.js pages
│   │   └── styles/              # Tailwind CSS
│   └── package.json
├── docs/             # This documentation
├── README.md
└── CLAUDE.md
```

## Next Steps

- [Architecture](architecture.md) — Understand how the system fits together
- [API Reference](api-reference.md) — Explore the available endpoints
- [Configuration](configuration.md) — Full environment and config details
