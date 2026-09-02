from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict
from uuid import UUID

class StudentProfile(BaseModel):
    display_name: str = "Maya Patel"
    default_language: str = "Hinglish"
    learning_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    learning_goal: Optional[str] = "Understand Ohm's Law and Circuit Relationships"

class LessonSegment(BaseModel):
    sequence: int
    concept: str
    duration_minutes: int
    strategy: Literal["analogy", "example", "formula", "step_by_step", "visual"]
    visual_type: Literal["circuit", "water_pipe", "equation", "graph", "diagram", "code"]
    has_checkpoint: bool = True

class LessonPlan(BaseModel):
    topic: str
    language: str
    level: str
    segments: List[LessonSegment]

class CheckpointQuestion(BaseModel):
    concept: str
    prompt: str
    options: Dict[str, str] # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_option: str
    formula: Optional[str] = None

class CheckpointEvaluation(BaseModel):
    is_correct: bool
    correct_option: str
    formula: Optional[str] = None
    feedback: str
    mastery_before_pct: int
    mastery_after_pct: int
    misconception_detected: Optional[str] = None
    remediation_strategy: Optional[str] = None
    remediation_visual: Optional[str] = None
