from fastapi import APIRouter, Request

from app.models.schemas import ChatRequest, ChatResponse, SearchQuery
from app.services.llm_service import chat_with_ai

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest, request: Request):
    """Handle chat requests and return AI responses."""
    response = chat_with_ai(req.message, client=request.app.state.http_client)
    return ChatResponse(response=response)


@router.post("/search")
def search_endpoint(query: SearchQuery, request: Request):
    """Search documents based on query."""
    search_service = request.app.state.search_service
    results = search_service.search(query.query, query.top_k)
    return {
        "query": query.query,
        "results": [{"document": doc, "score": float(score)} for doc, score in results],
    }


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
