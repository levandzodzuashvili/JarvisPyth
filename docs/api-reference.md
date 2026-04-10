# API Reference

The Python Jarvis backend exposes three HTTP endpoints. All request and response bodies are JSON. Successful responses return HTTP `200`.

**Authentication:** None. All endpoints are open with no API key or token required.

> FastAPI also auto-generates interactive API documentation:
> - **Swagger UI:** `http://localhost:8000/docs`
> - **ReDoc:** `http://localhost:8000/redoc`

## Endpoints

### `POST /chat`

Send a message and receive an AI-generated response via the Groq LLM.

**Request Body:**

| Field     | Type   | Required | Description          |
| --------- | ------ | -------- | -------------------- |
| `message` | string | yes      | The user's message   |

**Response Body:**

| Field      | Type   | Description                                  |
| ---------- | ------ | -------------------------------------------- |
| `response` | string | AI-generated reply (or error message on failure) |

**Example:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is BM25?"}'
```

```json
{
  "response": "BM25 (Best Match 25) is a ranking function used in information retrieval..."
}
```

**Error behavior:** On failure, the response field contains an error string (e.g., `"Error: Request to Groq API timed out"`). The HTTP status code is still `200`.

---

### `POST /search`

Search the in-memory document collection using BM25 ranking. This endpoint is not yet used by the frontend UI.

**Request Body:**

| Field   | Type   | Required | Default | Description                     |
| ------- | ------ | -------- | ------- | ------------------------------- |
| `query` | string | yes      | —       | Search query text               |
| `top_k` | int    | no       | `5`     | Maximum number of results       |

**Response Body:**

| Field     | Type   | Description            |
| --------- | ------ | ---------------------- |
| `query`   | string | The original query     |
| `results` | array  | Ranked search results  |

Each result object:

| Field      | Type   | Description                |
| ---------- | ------ | -------------------------- |
| `document` | string | The matched document text  |
| `score`    | float  | BM25 relevance score       |

**Example:**

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "office equipment", "top_k": 3}'
```

```json
{
  "query": "office equipment",
  "results": [
    {"document": "office equipment policy", "score": 1.39},
    {"document": "office furniture policy", "score": 0.29}
  ]
}
```

**Note:** Only documents with a score > 0 are returned. Results are sorted by score (descending).

**Error behavior:** This endpoint has no error handling. If the search service fails, the server returns an HTTP `500` with a FastAPI default error body.

---

### `GET /health`

Health check endpoint.

**Response Body:**

| Field    | Type   | Description     |
| -------- | ------ | --------------- |
| `status` | string | Always `"ok"`   |

**Example:**

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "ok"
}
```

## Pydantic Models

All request/response models are defined in `backend/app/models/schemas.py`.

| Model            | Fields                                 | Used By        |
| ---------------- | -------------------------------------- | -------------- |
| `ChatRequest`    | `message: str`                         | `POST /chat`   |
| `ChatResponse`   | `response: str`                        | `POST /chat`   |
| `SearchQuery`    | `query: str`, `top_k: Optional[int]=5` | `POST /search` |
| `DocumentUpload` | `content: str`, `title: str`           | Not yet wired  |

## Sample Documents

The backend initializes with these sample documents in `backend/app/api/routes.py`:

- `"office equipment policy"`
- `"office furniture policy"`
- `"office travel policy"`
- `"employee benefits and insurance"`
- `"workplace safety guidelines"`

These are loaded into the BM25 index at startup and reset on every server restart.

## See Also

- [Architecture](architecture.md) — Request flow diagrams
- [Backend Guide](backend.md) — Service implementation details
- [Configuration](configuration.md) — CORS settings and ports
