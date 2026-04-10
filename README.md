# Python Jarvis

An AI-powered chatbot application for document analysis and intelligent Q&A.

## Project Structure

```
python-jarvis-v1/
├── frontend/                 # Next.js TypeScript application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Next.js pages
│   │   └── styles/         # CSS & Tailwind styles
│   ├── public/             # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── next.config.js
├── backend/                 # FastAPI Python application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app initialization
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py   # API endpoints
│   │   ├── services/       # Business logic
│   │   │   ├── llm_service.py      # Groq LLM integration
│   │   │   └── document_service.py # Document search (BM25)
│   │   ├── models/         # Pydantic schemas
│   │   │   └── schemas.py
│   │   └── utils/
│   │       └── config.py   # Configuration
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn
- Groq API key

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create a Python virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

5. Run the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Features

- **Chat Interface**: Real-time chatbot powered by Groq's LLM
- **Document Search**: BM25-based document retrieval
- **Modern UI**: Built with React, Next.js, and Tailwind CSS
- **Type Safety**: TypeScript for both frontend and Python type hints
- **CORS Enabled**: Seamless frontend-backend communication

## API Endpoints

- `POST /chat` - Send a message and get AI response
- `POST /search` - Search documents
- `GET /health` - Health check endpoint

## Development

### Adding New Features

**Backend:**

1. Create new service in `app/services/`
2. Add API route in `app/api/routes.py`
3. Update schemas in `app/models/schemas.py`

**Frontend:**

1. Create new component in `src/components/`
2. Add page in `src/pages/`

## Environment Variables

Create a `.env` file in the backend directory:

```
GROQ_API_KEY=your_api_key_here
```

## Documentation

Full project documentation is available in the [`docs/`](docs/index.md) folder:

- [Getting Started](docs/getting-started.md) — Setup guide
- [Architecture](docs/architecture.md) — System design and request flows
- [API Reference](docs/api-reference.md) — Endpoint specs and examples
- [Backend Guide](docs/backend.md) — Service layer deep dive
- [Frontend Guide](docs/frontend.md) — Component and styling guide
- [Configuration](docs/configuration.md) — All config options
- [Contributing](docs/contributing.md) — Development workflow

## License

MIT License
