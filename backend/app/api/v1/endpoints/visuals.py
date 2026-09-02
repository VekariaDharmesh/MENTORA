"""
Subject-Aware Visual Engine Endpoints
"""

from fastapi import APIRouter, Depends
from app.core.deps import get_visual_service
from app.services.visual_engine import VisualEngineService
from app.schemas.visual import RenderVisualPayload

router = APIRouter()

@router.post("/visuals/render", tags=["Visual Engine"])
async def render_visual(
    payload: RenderVisualPayload,
    visual_service: VisualEngineService = Depends(get_visual_service)
):
    """
    Renders dynamic SVG visuals (electrical circuit or hydraulic water pipe).
    """
    if payload.visual_type == "water_pipe":
        return visual_service.render_water_pipe_svg(pipe_width=payload.pipe_width or "Narrow")
    return visual_service.render_circuit_svg(
        voltage=payload.voltage or 9.0,
        resistance=payload.resistance or 10.0,
        switch_closed=payload.switch_closed if payload.switch_closed is not None else True
    )
