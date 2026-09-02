"""
Advanced Features Pydantic Schemas
Contracts for targeted homework generation and revision sprint modes.
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class GenerateHomeworkPayload(BaseModel):
    weak_areas: Optional[List[str]] = Field(default=None, description="List of diagnosed misconception areas")

class StartRevisionPayload(BaseModel):
    topic: str = Field(default="Ohm's Law", description="Topic to revise")
