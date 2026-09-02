"""
Production Support & Telemetry Schemas
Contracts for analytics event logging, job lifecycle, and accessibility configuration.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class LogAnalyticsPayload(BaseModel):
    session_id: str = Field(default="demo_session", description="Active learning session ID")
    event_type: str = Field(..., description="Action type ('pause', 'checkpoint_submit', etc.)")
    metadata: Optional[Dict[str, Any]] = None

class JobControlPayload(BaseModel):
    job_id: str = Field(..., description="Target pipeline job identifier")

class AccessibilityPayload(BaseModel):
    student_id: str = Field(default="default_student", description="Student ID")
    settings: Dict[str, Any] = Field(..., description="Accessibility settings dictionary")
