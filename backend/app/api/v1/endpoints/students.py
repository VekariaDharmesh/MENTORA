"""
Student Learner Model & Knowledge State Endpoints
"""

from fastapi import APIRouter, Depends
from app.core.deps import get_learner_service
from app.services.learner_model import LearnerModelService

router = APIRouter()

@router.get("/students/knowledge-state", tags=["Learner Model"])
async def get_student_knowledge_state(
    learner_service: LearnerModelService = Depends(get_learner_service)
):
    """
    Returns current mastery percentages, confidence, and detected misconceptions.
    """
    return learner_service.get_knowledge_state()
