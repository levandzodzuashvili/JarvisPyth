from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse, SearchQuery
from app.services.llm_service import chat_with_ai
from app.services.document_service import DocumentSearchService

router = APIRouter()

# Initialize service
search_service = DocumentSearchService()

# Sample documents for testing
sample_docs = [
    "office equipment policy",
    "office furniture policy",
    "office travel policy",
    "employee benefits and insurance",
    "workplace safety guidelines"
]
search_service.add_documents(sample_docs)


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """Handle chat requests and return AI responses."""
    try:
        response = chat_with_ai(req.message)
        return ChatResponse(response=response)
    except Exception as e:
        return ChatResponse(response=f"Error: {str(e)}")


@router.post("/search")
def search_endpoint(query: SearchQuery):
    """Search documents based on query."""
    results = search_service.search(query.query, query.top_k)
    return {
        "query": query.query,
        "results": [{"document": doc, "score": float(score)} for doc, score in results]
    }


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
