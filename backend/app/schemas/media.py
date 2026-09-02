"""
Media Engine Pydantic Schemas
Contracts for TTS voice synthesis and video fallback controls.
"""

from pydantic import BaseModel, Field

class SynthesizeVoicePayload(BaseModel):
    text: str = Field(..., description="Script text to synthesize")
    language: str = Field(default="Hinglish", description="Spoken language")
    voice_id: str = Field(default="dr_aris_calm", description="Voice profile identifier")

class MediaFallbackPayload(BaseModel):
    job_id: str = Field(..., description="Target job identifier")
    error_reason: str = Field(default="Avatar video pipeline timeout", description="Degradation cause")
