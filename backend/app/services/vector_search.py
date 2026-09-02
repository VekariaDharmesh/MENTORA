import math
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.db.models import DocumentChunk
import google.generativeai as genai
import os

class VectorSearchService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key and self.api_key != "your_gemini_api_key":
            self.configured = True
        else:
            self.configured = False
            
    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2:
            return 0.0
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(a * a for a in v1))
        magnitude2 = math.sqrt(sum(b * b for b in v2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)
        
    def search(self, query: str, db: Session, top_k: int = 3) -> List[DocumentChunk]:
        """
        Embeds the query and performs in-memory cosine similarity against chunks.
        """
        if not self.configured:
            # Fallback: exact substring search or just return first 3
            chunks = db.query(DocumentChunk).filter(DocumentChunk.content.ilike(f"%{query}%")).limit(top_k).all()
            if not chunks:
                chunks = db.query(DocumentChunk).limit(top_k).all()
            return chunks

        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = result['embedding']
        except Exception as e:
            return db.query(DocumentChunk).limit(top_k).all()

        # Fetch all chunks with embeddings
        chunks = db.query(DocumentChunk).filter(DocumentChunk.embedding.isnot(None)).all()
        
        # Calculate similarity
        scored_chunks = []
        for chunk in chunks:
            score = self._cosine_similarity(query_embedding, chunk.embedding)
            scored_chunks.append((score, chunk))
            
        # Sort by score descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        # Return top k
        return [chunk for score, chunk in scored_chunks[:top_k]]
