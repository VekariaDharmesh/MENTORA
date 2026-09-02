"""
Health Check Endpoint
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "engine": "AI Teacher Pedagogical Engine",
        "mode": "Socratic Adaptive Mode",
        "version": "1.0.0"
    }
