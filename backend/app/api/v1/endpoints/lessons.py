"""
Lesson Planner Endpoints
Dynamically generates multi-segment structured curricula powered by LLM.
"""

from fastapi import APIRouter, Depends
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel

from app.core.deps import get_llm_service
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
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Dynamically generates a personalized curriculum using LLM intelligence.
    """
    plan = await llm_service.generate_lesson_plan(
        topic=payload.topic,
        level=payload.level,
        duration_minutes=payload.duration_minutes,
        language=payload.language,
        context=payload.document_context or payload.objective
    )
    
    plan["lesson_id"] = f"lesson-{uuid4().hex[:8]}"
    return plan
