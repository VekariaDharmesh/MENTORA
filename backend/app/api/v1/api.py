"""
API V1 Unified Router
Aggregates all modular endpoint routers into the /api/v1 root namespace.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    documents,
    concepts,
    students,
    lessons,
    teaching,
    visuals,
    multilingual,
    media,
    assessment,
    advanced,
    analytics,
    ws_teaching,
)

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(health.router)
api_router.include_router(documents.router)
api_router.include_router(concepts.router)
api_router.include_router(students.router)
api_router.include_router(lessons.router)
api_router.include_router(teaching.router)
api_router.include_router(visuals.router)
api_router.include_router(multilingual.router)
api_router.include_router(media.router)
api_router.include_router(assessment.router)
api_router.include_router(advanced.router)
api_router.include_router(analytics.router)
api_router.include_router(ws_teaching.router)
