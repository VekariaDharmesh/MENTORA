"""
Teaching Engine Pydantic Schemas
Contracts for checkpoint answering, Teacher Brain inspection, and contextual inquiries.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class CheckpointAnswerPayload(BaseModel):
    choice: str = Field(..., description="Student choice ('A', 'B', 'C', or 'D')")
    concept: str = Field(default="Resistance", description="Active learning concept")

class ContextualAskPayload(BaseModel):
    question: str = Field(..., description="Student inquiry text")
    concept: str = Field(default="Resistance", description="Active learning concept")

class TeacherBrainResponse(BaseModel):
    status: str
    current_concept: str
    student_mastery_pct: int
    confidence_pct: int
    detected_misconception: Optional[str] = None
    decision: str
    strategy: str
    reason: str
    next_action: str
    knowledge_source: str
