# Backend Guide

The backend is a FastAPI application located in `backend/app/`. It handles API requests, communicates with the Groq LLM, and provides BM25 document search.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, CORS middleware
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # Endpoint handlers
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py      # Groq API integration
│   │   └── document_service.py # BM25 search engine
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic request/response models
│   └── utils/
│       ├── __init__.py
│       └── config.py           # Environment config loader
├── requirements.txt
└── .env.example
```

## Service Layer

### LLM Service (`app/services/llm_service.py`)

Handles communication with the Groq API using an OpenAI-compatible REST interface.

**Key function: `chat_with_ai(user_message: str) -> str`**
- Constructs a messages array with a system prompt and the user message
- System prompt: *"You are a helpful assistant that can analyze documents and answer questions about them."*
- Delegates to `create_groq_response()`

**Key function: `create_groq_response(messages: list, model: str) -> str`**
- Sends a POST request to `https://api.groq.com/openai/v1/chat/completions`
- Uses synchronous `httpx.Client` with a 30-second timeout
- Headers: `Authorization: Bearer <GROQ_API_KEY>`, `Content-Type: application/json`
- Default parameters:
  - `model`: `llama-3.1-8b-instant`
  - `max_tokens`: 512
  - `temperature`: 0.7
- Error handling covers: timeout, HTTP errors, unexpected response format

**Key function: `parse_groq_response(data: dict) -> str`**
- Extracts `choices[0].message.content` from the Groq response
- Raises `ValueError` if the response format is unexpected

### Document Search Service (`app/services/document_service.py`)

Provides BM25-based document search using the `rank_bm25` library.

**Class: `DocumentSearchService`**

| Method | Signature | Description |
| ------ | --------- | ----------- |
| `add_documents` | `(docs: List[str])` | Index documents using BM25Okapi. Tokenization: whitespace split. |
| `search` | `(query: str, top_k: int = 5) -> List[Tuple[str, float]]` | Score query against index, return top-k results with score > 0, sorted descending. |

**How BM25 works here:**
1. Documents are tokenized by splitting on whitespace (no stemming or lemmatization)
2. A BM25Okapi index is built from the tokenized corpus
3. Queries are tokenized the same way
4. Each document receives a relevance score; only positive scores are returned

## Adding a New Endpoint

1. **Define the schema** in `app/models/schemas.py`:
   ```python
   class MyRequest(BaseModel):
       field_name: str

   class MyResponse(BaseModel):
       result: str
   ```

2. **Add the route** in `app/api/routes.py`:
   ```python
   @router.post("/my-endpoint")
   def my_endpoint(req: MyRequest):
       # Call your service
       result = my_service.do_something(req.field_name)
       return MyResponse(result=result)
   ```

3. **Implement the service** in `app/services/my_service.py` (see next section).

## Adding a New Service

1. Create `app/services/my_service.py`:
   ```python
   class MyService:
       def __init__(self):
           # Initialize resources
           pass

       def do_something(self, input: str) -> str:
           # Business logic here
           return f"Processed: {input}"
   ```

2. Import and instantiate it in `app/api/routes.py`:
   ```python
   from app.services.my_service import MyService
   my_service = MyService()
   ```

## Dependencies

| Package          | Version | Purpose                                |
| ---------------- | ------- | -------------------------------------- |
| fastapi          | 0.104.1 | Web framework                          |
| uvicorn          | 0.24.0  | ASGI server                            |
| pydantic         | 2.5.0   | Data validation and serialization      |
| python-dotenv    | 1.0.0   | `.env` file loading                    |
| httpx            | 0.25.2  | HTTP client (Groq API calls)           |
| rank-bm25        | 0.2.2   | BM25 document ranking algorithm        |
| python-multipart | 0.0.6   | Multipart form data support            |

## See Also

- [API Reference](api-reference.md) — Endpoint specifications and examples
- [Architecture](architecture.md) — System overview and request flows
- [Configuration](configuration.md) — Environment variables and CORS settings
