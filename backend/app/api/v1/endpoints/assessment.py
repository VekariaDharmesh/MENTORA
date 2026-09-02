"""
Assessment & Learning Report Endpoints
"""

from fastapi import APIRouter, Depends
from app.core.deps import get_assessment_service
from app.services.assessment_engine import AssessmentEngineService
from app.schemas.assessment import SubmitAssessmentPayload

router = APIRouter()

@router.get("/assessment/generate", tags=["Assessment"])
async def generate_assessment(
    assessment_service: AssessmentEngineService = Depends(get_assessment_service)
):
    """
    Generates an 8-question active diagnostic assessment based on concept graph.
    """
    return assessment_service.generate_assessment()

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
    return assessment_service.grade_assessment(answers)
