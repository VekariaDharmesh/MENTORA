from pydantic import BaseModel, Field
from typing import Optional

class CheckpointAnswerPayload(BaseModel):
    choice: str = Field(..., description="Student's selected text or option letter")
    concept: str = Field(..., description="Active learning concept")
    question: str = Field(..., description="The prompt of the question that was asked")
    correct_option: str = Field(..., description="The correct answer text or option letter")

class ContextualAskPayload(BaseModel):
    question: str = Field(..., description="Student inquiry text")
    concept: str = Field(default="Resistance", description="Active learning concept")
