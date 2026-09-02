"""
Advanced Features Endpoints (Flashcards, Notes, Homework, Revision)
"""

from fastapi import APIRouter, Depends
from app.core.deps import get_advanced_service
from app.services.advanced_features import AdvancedFeaturesService
from app.schemas.advanced import GenerateHomeworkPayload, StartRevisionPayload

router = APIRouter()

@router.get("/advanced/flashcards", tags=["Advanced Features"])
async def get_flashcards(
    topic: str = "Electricity",
    advanced_service: AdvancedFeaturesService = Depends(get_advanced_service)
):
    """
    Generates tactile Socratic flashcards for active recall revision.
    """
    return {"topic": topic, "flashcards": advanced_service.generate_flashcards(topic)}

@router.get("/advanced/notes", tags=["Advanced Features"])
async def get_study_notes(
    topic: str = "Electricity",
    advanced_service: AdvancedFeaturesService = Depends(get_advanced_service)
):
    """
    Generates Cornell-style study notes for the Warm Study Desk.
    """
    return advanced_service.generate_notes(topic)

@router.post("/advanced/homework", tags=["Advanced Features"])
async def generate_homework(
    payload: GenerateHomeworkPayload,
    advanced_service: AdvancedFeaturesService = Depends(get_advanced_service)
):
    """
    Generates targeted practice problems addressing diagnosed misconceptions.
    """
    return {
        "weak_areas": payload.weak_areas or ["Resistance", "Ohm's Law"],
        "problems": advanced_service.generate_homework(payload.weak_areas)
    }

@router.post("/advanced/revision", tags=["Advanced Features"])
async def start_revision_mode(
    payload: StartRevisionPayload,
    advanced_service: AdvancedFeaturesService = Depends(get_advanced_service)
):
    """
    Initializes a focused 5-minute targeted revision sprint with water-pipe tactile demonstrations.
    """
    return advanced_service.start_revision_mode(payload.topic)
