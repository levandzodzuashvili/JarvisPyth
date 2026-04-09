from rank_bm25 import BM25Okapi
from typing import List, Tuple


class DocumentSearchService:
    """Service for searching documents using BM25 algorithm."""
    
    def __init__(self):
        self.documents: List[str] = []
        self.bm25: BM25Okapi = None
    
    def add_documents(self, docs: List[str]):
        """Add documents to the search index."""
        self.documents = docs
        tokenized_docs = [doc.split() for doc in docs]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Search documents and return top k results with scores."""
        if not self.bm25:
            return []
        
        query_tokens = query.split()
        scores = self.bm25.get_scores(query_tokens)
        
        # Get top k results
        top_indices = scores.argsort()[-top_k:][::-1]
        results = [(self.documents[i], scores[i]) for i in top_indices if scores[i] > 0]
        
        return results
