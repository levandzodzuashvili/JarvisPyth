from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class DocumentUpload(BaseModel):
    content: str
    title: str


class SearchQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5
