from typing import Dict, Any, Optional
from app.services.llm_service import LLMService

class TeachingState:
    INIT = "INIT"
    UNDERSTAND = "UNDERSTAND"
    PLAN = "PLAN"
    INTRODUCE = "INTRODUCE"
    EXPLAIN = "EXPLAIN"
    DEMONSTRATE = "DEMONSTRATE"
    QUESTION = "QUESTION"
    EVALUATE = "EVALUATE"
    REMEDIATE = "REMEDIATE"
    ADVANCE = "ADVANCE"
    COMPLETE = "COMPLETE"

class TeachingStateMachine:
    def __init__(self, llm_service: LLMService):
        self.lesson_id = None
        self.current_state = TeachingState.EXPLAIN
        self.current_concept = ""
        self.llm_service = llm_service
        self.teacher_brain_state = {
            "status": "Teaching · Active",
            "current_concept": "",
            "student_mastery_pct": 50,
            "confidence_pct": 0,
            "detected_misconception": "None",
            "decision": "ADVANCE",
            "strategy": "Explain",
            "reason": "Proceeding with standard curriculum.",
            "next_action": "Wait for student response",
            "knowledge_source": "Topic Profile"
        }

    async def evaluate_checkpoint(self, choice: str, concept: str, question: str, correct_option: str) -> Dict[str, Any]:
        """
        Dynamically evaluates the student's checkpoint response using the LLM and deterministic state machine.
        """
        self.current_state = TeachingState.EVALUATE
        self.current_concept = concept
        
        # Use LLM to diagnose response dynamically
        eval_result = await self.llm_service.evaluate_student_answer(
            concept=concept,
            question=question,
            student_answer=choice,
            correct_option=correct_option
        )
        
        is_correct = eval_result.get("is_correct", False)
        
        if is_correct:
            self.current_state = TeachingState.ADVANCE
            self.teacher_brain_state.update({
                "decision": "ADVANCE",
                "next_action": "Advance to next concept",
                "student_mastery_pct": min(100, self.teacher_brain_state["student_mastery_pct"] + int(eval_result.get("mastery_delta", 0.1) * 100)),
                "confidence_pct": 90,
                "detected_misconception": "None",
                "reason": "Student demonstrated correct understanding."
            })

            return {
                "is_correct": True,
                "correct_option": correct_option,
                "concept": concept,
                "heading": eval_result.get("heading", "Exactly."),
                "explanation": eval_result.get("feedback", "Great job."),
                "mastery_before": self.teacher_brain_state["student_mastery_pct"] - 10,
                "mastery_after": self.teacher_brain_state["student_mastery_pct"],
                "next_action": "Continue to next concept →",
                "next_state": TeachingState.ADVANCE
            }
        else:
            self.current_state = TeachingState.REMEDIATE
            strategy = eval_result.get("strategy", "Analogy")
            misconception = eval_result.get("misconception", "Unknown error")
            
            self.teacher_brain_state.update({
                "decision": "RE-EXPLAIN",
                "strategy": strategy,
                "student_mastery_pct": max(0, self.teacher_brain_state["student_mastery_pct"] - 5),
                "detected_misconception": misconception,
                "reason": f"Detected: {misconception}",
                "next_action": "Provide new adapted explanation"
            })

            return {
                "is_correct": False,
                "correct_option": correct_option,
                "concept": concept,
                "heading": eval_result.get("heading", "Let's look at this another way."),
                "subheading": "I noticed a small misunderstanding.",
                "student_answer": choice,
                "teacher_observation": eval_result.get("feedback", "The relationship appears misunderstood."),
                "misconception_category": misconception,
                "original_approach": "Standard Explanation",
                "new_approach": strategy,
                "adapted_label": "Teacher adapted the lesson",
                "next_action": "Try a different explanation →",
                "next_state": TeachingState.REMEDIATE
            }

    def get_teacher_brain(self) -> Dict[str, Any]:
        return self.teacher_brain_state
