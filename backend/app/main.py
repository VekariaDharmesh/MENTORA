"""
AI Teacher — Production FastAPI Application Entrypoint
Structured with Clean Architecture & SOLID Software Engineering Principles.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.api.v1.api import api_router

def create_application() -> FastAPI:
    """
    Application factory initializing middleware, routes, and metadata.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Cognitive Socratic Teaching Engine with RAG, Learner Model, and Misconception Adaptation.",
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount unified API v1 router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    # Also mount health check at root /health for convenience
    from app.api.v1.endpoints.health import router as health_router
    app.include_router(health_router)

    return app

app = create_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
