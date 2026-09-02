"""
Media & Voice Synthesis Endpoints
"""

from fastapi import APIRouter, Depends
from app.core.deps import get_media_service
from app.services.media_engine import MediaEngineService
from app.schemas.media import SynthesizeVoicePayload, MediaFallbackPayload

router = APIRouter()

@router.post("/media/voice/synthesize", tags=["Media Engine"])
async def synthesize_voice(
    payload: SynthesizeVoicePayload,
    media_service: MediaEngineService = Depends(get_media_service)
):
    """
    Synthesizes voice segment with status tracking and playback URL.
    """
    return media_service.synthesize_voice(
        text=payload.text,
        language=payload.language,
        voice_id=payload.voice_id
    )

@router.post("/media/fallback", tags=["Media Engine"])
async def trigger_media_fallback(
    payload: MediaFallbackPayload,
    media_service: MediaEngineService = Depends(get_media_service)
):
    """
    Gracefully downgrades from full avatar video to audio + visual canvas + captions.
    """
    return media_service.fallback_to_audio_only(
        job_id=payload.job_id,
        error_reason=payload.error_reason
    )

@router.get("/media/health", tags=["Media Engine"])
async def media_health(
    media_service: MediaEngineService = Depends(get_media_service)
):
    """
    Health check for all media generation providers (LLM, TTS, Avatar, FFmpeg, Storage).
    """
    return media_service.get_health()

@router.get("/media/job/{job_id}", tags=["Media Engine"])
async def get_media_job(
    job_id: str,
    media_service: MediaEngineService = Depends(get_media_service)
):
    """
    Get real-time progress and status of a video generation job.
    """
    from fastapi import HTTPException
    job = media_service.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
