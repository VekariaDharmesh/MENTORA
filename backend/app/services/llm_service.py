import os
import json
import logging
from typing import Dict, Any, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key and self.api_key != "your_gemini_api_key":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.flash_model = genai.GenerativeModel('gemini-1.5-flash')
            self.configured = True
        else:
            self.configured = False
            logger.warning("GEMINI_API_KEY is missing or default. LLM Service will fail if called.")

    def is_configured(self) -> bool:
        return self.configured

    async def generate_lesson_plan(
        self, 
        topic: str, 
        level: str, 
        duration_minutes: int, 
        language: str, 
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dynamically generates a personalized curriculum using LLM intelligence.
        """
        if not self.is_configured():
            return {
                "topic": topic,
                "objective": "Fallback objective due to missing API key.",
                "level": level,
                "duration_minutes": duration_minutes,
                "language": language,
                "segments": [
                    {
                        "sequence": 1,
                        "concept": "Foundational Concept",
                        "duration": 5,
                        "strategy": "analogy",
                        "visual_type": "diagram",
                        "caption": "Welcome. This is a fallback lesson since the Gemini API key is not configured.",
                        "has_checkpoint": True,
                        "checkpoint_question": {
                            "prompt": "What happens to current if resistance increases while voltage stays constant?",
                            "options": {"A": "It increases", "B": "It decreases", "C": "Stays the same", "D": "Zero"},
                            "correct": "B"
                        }
                    }
                ]
            }
        
        prompt = f"""
        You are an expert pedagogical engine for the MENTORE AI Teacher platform.
        Create a highly structured lesson plan.
        Topic: {topic}
        Student Level: {level}
        Duration: {duration_minutes} minutes
        Language: {language}
        Context/Document excerpt: {context if context else 'None'}

        Output MUST be valid JSON matching this schema EXACTLY:
        {{
            "topic": "string",
            "objective": "string",
            "level": "string",
            "duration_minutes": {duration_minutes},
            "language": "{language}",
            "segments": [
                {{
                    "sequence": 1,
                    "concept": "string",
                    "duration": int,
                    "strategy": "analogy|example|formula|step_by_step|visual",
                    "visual_type": "diagram|circuit|water_pipe|equation|graph",
                    "caption": "string (the exact script the avatar will say)",
                    "has_checkpoint": bool,
                    "checkpoint_question": {{
                        "prompt": "string",
                        "options": {{"A": "string", "B": "string", "C": "string", "D": "string"}},
                        "correct": "A|B|C|D"
                    }} // ONLY if has_checkpoint is true
                }}
            ]
        }}
        
        Rules:
        - Total duration of all segments should sum to approximately {duration_minutes} minutes.
        - Ensure explanations and the 'caption' match the requested language ({language}).
        - Keep the lesson engaging. The final segment MUST have a checkpoint.
        - DO NOT wrap the output in markdown blocks like ```json, just return raw JSON.
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM lesson output: {response.text}")
            raise ValueError("LLM generated invalid JSON.")

    async def evaluate_student_answer(self, concept: str, question: str, student_answer: str, correct_option: str) -> Dict[str, Any]:
        """
        Dynamically evaluates student response, detects misconception, and determines adaptive remediation.
        """
        if not self.is_configured():
            is_correct = (student_answer.strip().upper() == correct_option.strip().upper())
            if is_correct:
                return {
                    "is_correct": True,
                    "concept": concept,
                    "heading": "Exactly right.",
                    "feedback": "Fallback evaluation: Correct answer.",
                    "misconception": None,
                    "decision": "ADVANCE",
                    "strategy": "explain",
                    "visual_recommendation": "none",
                    "mastery_delta": 0.1
                }
            else:
                return {
                    "is_correct": False,
                    "concept": concept,
                    "heading": "Let's look at this another way.",
                    "feedback": "Fallback evaluation: Incorrect answer. Inverse relationship confused.",
                    "misconception": "concept_reversal",
                    "decision": "RE-EXPLAIN",
                    "strategy": "analogy",
                    "visual_recommendation": "water_pipe",
                    "mastery_delta": -0.05
                }
        
        prompt = f"""
        You are the evaluation engine for MENTORE.
        Concept: {concept}
        Question: {question}
        Student chose: {student_answer}
        The correct option is: {correct_option}

        If the student is incorrect, diagnose WHY they are incorrect (misconception type).
        
        Return exactly this JSON schema:
        {{
            "is_correct": bool,
            "concept": "string",
            "heading": "string (e.g., 'Exactly right' or 'Let's look at this another way')",
            "feedback": "string (brief feedback)",
            "misconception": "string or null (e.g., 'concept_reversal', 'unit_confusion', 'inverse_relationship_confusion')",
            "decision": "ADVANCE" or "RE-EXPLAIN",
            "strategy": "string (e.g., 'analogy', 'visual', 'step_by_step')",
            "visual_recommendation": "string",
            "mastery_delta": float (e.g., 0.1 for correct, -0.05 for incorrect)
        }}
        
        DO NOT wrap the output in markdown blocks.
        """
        
        response = self.flash_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM evaluation output: {response.text}")
            raise ValueError("LLM generated invalid JSON.")

