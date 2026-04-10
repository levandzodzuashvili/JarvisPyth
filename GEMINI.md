# GEMINI.md

## Project Overview
**Python Jarvis** is an AI-powered chatbot application designed for document analysis and intelligent Q&A. It utilizes a FastAPI backend integrated with the Groq LLM API and a Next.js frontend for a modern user experience.

- **Architecture:** Two-tier (Next.js Frontend + FastAPI Backend)
- **Backend:** Python 3.9+, FastAPI, Pydantic, Groq LLM (Llama 3.1), BM25 Document Search (`rank-bm25`)
- **Frontend:** React 18, Next.js 14 (Pages Router), TypeScript, Tailwind CSS
- **Key Features:** Real-time chat, BM25-based keyword document retrieval, and CORS-enabled communication.

## Project Structure
```text
/
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── api/            # Route handlers (chat, search, health)
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # LLM (Groq) and Document Search logic
│   │   ├── utils/          # Configuration and env loading
│   │   └── main.py         # App entry point and CORS config
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── components/     # UI components (Chat.tsx)
│   │   ├── pages/          # Next.js pages (index.tsx)
│   │   └── styles/         # Global CSS and Tailwind
│   └── package.json        # Node.js dependencies and scripts
└── docs/                   # Detailed architectural and API documentation
```

## Building and Running

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key (Set in `backend/.env`)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env      # Configure GROQ_API_KEY
uvicorn app.main:app --reload
```
- **API URL:** `http://localhost:8000`
- **Documentation:** `http://localhost:8000/docs` (Swagger UI)

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
- **App URL:** `http://localhost:3000`

### Key Commands
- **Build Frontend:** `npm run build`
- **Lint Frontend:** `npm run lint`

## Development Conventions

### Backend
- **Service Pattern:** Business logic is encapsulated in `app/services/`.
- **Schemas:** All request/response bodies use Pydantic models in `app/models/schemas.py`.
- **CORS:** Configured in `main.py` to allow `localhost:3000`.
- **Search:** Document search uses an in-memory BM25 index; documents are currently hardcoded in `api/routes.py`.

### Frontend
- **Component Style:** Functional components with Tailwind CSS for utility-first styling.
- **State Management:** Local React `useState` for chat history and loading states.
- **Path Aliases:** Use `@/*` to refer to the `src/` directory.

## Known Issues & Notes
- **Port Mismatch:** `frontend/src/components/Chat.tsx` is currently hardcoded to fetch from `http://127.0.0.1:8001/chat`, while the backend defaults to `8000`. This requires adjustment for the chat to function.
- **Testing:** No automated testing framework (pytest/jest) is currently implemented.
- **Persistence:** Document search is purely in-memory and resets on backend restart.
