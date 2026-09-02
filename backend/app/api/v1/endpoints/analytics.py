"""
Production Telemetry & Accessibility Endpoints
"""

from fastapi import APIRouter, Depends
from typing import Optional
from app.core.deps import get_support_service
from app.services.production_support import ProductionSupportService
from app.schemas.analytics import LogAnalyticsPayload, JobControlPayload, AccessibilityPayload

router = APIRouter()

@router.post("/analytics/log", tags=["Production Support"])
async def log_session_event(
    payload: LogAnalyticsPayload,
    support_service: ProductionSupportService = Depends(get_support_service)
):
    """
    Logs session telemetry and pedagogical events.
    """
    return support_service.log_event(
        session_id=payload.session_id,
        event_type=payload.event_type,
        metadata=payload.metadata
    )

@router.get("/analytics/summary", tags=["Production Support"])
async def get_analytics_summary(
    session_id: Optional[str] = None,
    support_service: ProductionSupportService = Depends(get_support_service)
):
    """
    Returns aggregated metrics and event counts for the educator dashboard.
    """
    return support_service.get_analytics_summary(session_id=session_id)

@router.post("/media/cancel", tags=["Production Support"])
async def cancel_media_job(
    payload: JobControlPayload,
    support_service: ProductionSupportService = Depends(get_support_service)
):
    """
    Cleanly terminates an in-flight video/voice generation task.
    """
    return support_service.cancel_job(payload.job_id)

@router.post("/media/retry", tags=["Production Support"])
async def retry_media_job(
    payload: JobControlPayload,
    support_service: ProductionSupportService = Depends(get_support_service)
):
    """
    Retries a failed generation pipeline step.
    """
    return support_service.retry_job(payload.job_id)

@router.post("/accessibility/mode", tags=["Production Support"])
async def set_accessibility_mode(
    payload: AccessibilityPayload,
    support_service: ProductionSupportService = Depends(get_support_service)
):
    """
    Persists student accessibility preferences (reduced motion, captions, contrast).
    """
    return support_service.set_accessibility_mode(payload.student_id, payload.settings)

@router.get("/accessibility/mode", tags=["Production Support"])
async def get_accessibility_mode(
    student_id: str = "default_student",
    support_service: ProductionSupportService = Depends(get_support_service)
):
    """
    Fetches active accessibility preferences.
    """
    return support_service.get_accessibility_mode(student_id)
