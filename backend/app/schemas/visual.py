"""
Visual Engine Pydantic Schemas
Contracts for generating electrical circuits and hydraulic visual demonstrations.
"""

from pydantic import BaseModel
from typing import Optional

class RenderVisualPayload(BaseModel):
    visual_type: str = "circuit"
    voltage: Optional[float] = 9.0
    resistance: Optional[float] = 10.0
    switch_closed: Optional[bool] = True
    pipe_width: Optional[str] = "Narrow"
