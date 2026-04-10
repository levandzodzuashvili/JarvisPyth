from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class DocumentUpload(BaseModel):
    content: str
    title: str


class SearchQuery(BaseModel):
    query: str
    top_k: int = Field(default=5, gt=0, le=50)
