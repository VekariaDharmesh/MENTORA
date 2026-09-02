"""
Multilingual Translation Endpoints
"""

from fastapi import APIRouter, Depends
from app.core.deps import get_multilingual_service
from app.services.multilingual_engine import MultilingualEngineService
from app.schemas.multilingual import SwitchLanguagePayload

router = APIRouter()

@router.post("/teaching/language/switch", tags=["Multilingual Engine"])
async def switch_language(
    payload: SwitchLanguagePayload,
    multilingual_service: MultilingualEngineService = Depends(get_multilingual_service)
):
    """
    Translates concept explanation and captions into English, Hindi, or Hinglish.
    """
    return multilingual_service.translate_lesson_context(
        concept=payload.concept,
        target_language=payload.target_language
    )
