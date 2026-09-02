"""
Assessment Engine Pydantic Schemas
Contracts for diagnostic assessments, quizzes, and learning reports.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict

class SubmitAssessmentPayload(BaseModel):
    student_answers: Optional[Dict[str, str]] = Field(
        default=None,
        description="Map of question_id -> selected_option (e.g. {'q1': 'B'})"
    )
