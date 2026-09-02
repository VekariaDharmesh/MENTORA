"""
Multilingual Engine Pydantic Schemas
Contracts for translating concepts, scripts, and captions across languages.
"""

from pydantic import BaseModel, Field

class SwitchLanguagePayload(BaseModel):
    concept: str = Field(default="Voltage", description="Concept name to translate")
    target_language: str = Field(default="Hinglish", description="Target language ('English', 'Hindi', 'Hinglish')")
