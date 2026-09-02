from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.core.deps import get_assessment_service
from app.services.assessment_engine import AssessmentEngineService
from app.schemas.assessment import SubmitAssessmentPayload

router = APIRouter()

@router.get("/assessment/generate", tags=["Assessment"])
async def generate_assessment(
    topic: str = "Ohm's Law",
    assessment_service: AssessmentEngineService = Depends(get_assessment_service)
):
    """
    Generates an 8-question active diagnostic assessment based on concept graph.
    """
    return await assessment_service.generate_assessment(topic)

@router.post("/assessment/submit", tags=["Assessment"])
async def submit_assessment(
    payload: SubmitAssessmentPayload,
    assessment_service: AssessmentEngineService = Depends(get_assessment_service)
):
    """
    Evaluates student assessment and generates comprehensive editorial report.
    """
    answers = payload.student_answers or {
        "q1": "B", "q2": "A", "q3": "C", "q4": "B", 
        "q5": "B", "q6": "C", "q7": "A", "q8": "B"
    }
    # Currently we re-generate or use fallback data to grade because it's stateless.
    # In production, we'd fetch the saved quiz from DB.
    quiz_data = await assessment_service.generate_assessment("Ohm's Law")
    return await assessment_service.grade_assessment(answers, quiz_data)
