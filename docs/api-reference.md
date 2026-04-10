# API Reference

All endpoints are JSON. There is no authentication layer in this repository.

Interactive docs are available from FastAPI when the backend is running:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## `POST /chat`

Send one message to the Groq-backed chat service.

### Request

```json
{
  "message": "What is BM25?"
}
```

### Success Response

`200 OK`

```json
{
  "response": "BM25 is a ranking function used in information retrieval..."
}
```

### Error Responses

| Status | Body | Meaning |
| --- | --- | --- |
| `500` | `{"detail":"Chat service is unavailable"}` | Backend is missing required chat configuration such as `GROQ_API_KEY` |
| `504` | `{"detail":"Groq request timed out"}` | Upstream Groq call timed out |
| `502` | `{"detail":"Groq upstream error"}` | Groq returned a non-success HTTP status |
| `502` | `{"detail":"Invalid Groq response"}` | Groq returned an unexpected payload |
| `500` | `{"detail":"Internal server error"}` | Unexpected server-side failure |

## `POST /search`

Run BM25 search against the seeded in-memory sample document set.

### Request

```json
{
  "query": "office policy",
  "top_k": 3
}
```

### Validation

- `query` is required
- `top_k` defaults to `5`
- `top_k` must be an integer from `1` to `50`
- invalid `top_k` values return FastAPI validation errors (`422`)

### Success Response

```json
{
  "query": "office policy",
  "results": [
    {
      "document": "office equipment policy",
      "score": 0.87
    }
  ]
}
```

Only documents with a positive BM25 score are returned.

## `GET /health`

Lightweight readiness check.

```json
{
  "status": "ok"
}
```

## Seeded Sample Documents

At startup the backend indexes five sample strings:

- `office equipment policy`
- `office furniture policy`
- `office travel policy`
- `employee benefits and insurance`
- `workplace safety guidelines`

These are seeded during FastAPI lifespan setup in `backend/app/main.py`.
