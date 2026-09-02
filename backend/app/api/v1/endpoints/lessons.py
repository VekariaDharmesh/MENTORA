"""
Lesson Planner Endpoints
Dynamically generates multi-segment structured curricula powered by LLM.
"""

from fastapi import APIRouter, Depends
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_llm_service, get_vector_search
from app.services.vector_search import VectorSearchService
from app.services.llm_service import LLMService

class CreateLessonPayload(BaseModel):
    topic: str
    level: str = "beginner"
    duration_minutes: int = 20
    language: str = "Hinglish"
    objective: Optional[str] = None
    document_context: Optional[str] = None

router = APIRouter()

@router.post("/lessons/create", tags=["Lesson Planner"])
async def create_lesson(
    payload: CreateLessonPayload,
    llm_service: LLMService = Depends(get_llm_service),
    vector_search: VectorSearchService = Depends(get_vector_search),
    db: Session = Depends(get_db)
):
    """
    Dynamically generates a personalized curriculum using LLM intelligence and RAG.
    """
    context = payload.document_context
    if not context:
        # Perform RAG retrieval
        relevant_chunks = vector_search.search(payload.topic, db, top_k=3)
        if relevant_chunks:
            context = "\n\n".join([f"Source: {c.document.filename}\n{c.content}" for c in relevant_chunks])
        else:
            context = payload.objective

    plan = await llm_service.generate_lesson_plan(
        topic=payload.topic,
        level=payload.level,
        duration_minutes=payload.duration_minutes,
        language=payload.language,
        context=context
    )
    
    plan["lesson_id"] = f"lesson-{uuid4().hex[:8]}"
    return plan
