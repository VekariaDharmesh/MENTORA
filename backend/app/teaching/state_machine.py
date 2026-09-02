"""
Teaching Engine State Machine & Socratic Evaluator
Governs the pedagogical loop: Understand -> Plan -> Explain -> Demonstrate -> Question -> Evaluate -> Adapt -> Continue
"""

from typing import Dict, Any, Optional

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
    def __init__(self, lesson_id: str = "demo_lesson"):
        self.lesson_id = lesson_id
        self.current_state = TeachingState.EXPLAIN
        self.current_concept = "Resistance"
        self.current_segment_index = 3
        self.active_strategy = "formula"
        self.active_visual = "circuit"
        self.teacher_brain_state = {
            "status": "Teaching · Adaptive mode",
            "current_concept": "Resistance",
            "student_mastery_pct": 42,
            "confidence_pct": 94,
            "detected_misconception": "Inverse relationship confusion",
            "decision": "RE-EXPLAIN",
            "strategy": "Water-pipe analogy",
            "reason": "Student understands voltage and current individually but reversed their relationship with resistance.",
            "next_action": "Ask a new conceptual question",
            "knowledge_source": "Chapter 4 · Page 12"
        }

    def evaluate_checkpoint(self, choice: str, concept: str = "Resistance") -> Dict[str, Any]:
        """
        Evaluates the student's checkpoint response.
        Option B = Correct ("It decreases")
        Option A = Misconception ("It increases")
        """
        self.current_state = TeachingState.EVALUATE
        choice_upper = choice.strip().upper()

        if choice_upper == "B":
            self.current_state = TeachingState.ADVANCE
            self.teacher_brain_state["decision"] = "ADVANCE"
            self.teacher_brain_state["next_action"] = "Advance to Ohm's Law Unified Model"
            self.teacher_brain_state["student_mastery_pct"] = 78

            return {
                "is_correct": True,
                "correct_option": "B",
                "concept": concept,
                "heading": "Exactly.",
                "explanation": "As resistance increases, current decreases when voltage remains constant.",
                "formula": "I = V / R",
                "mastery_before": 68,
                "mastery_after": 78,
                "next_action": "Continue to Voltage →",
                "next_state": TeachingState.ADVANCE
            }
        else:
            self.current_state = TeachingState.REMEDIATE
            self.active_strategy = "water_pipe_analogy"
            self.active_visual = "water_pipe"
            self.teacher_brain_state["decision"] = "RE-EXPLAIN"
            self.teacher_brain_state["strategy"] = "Water-pipe analogy"
            self.teacher_brain_state["student_mastery_pct"] = 42

            return {
                "is_correct": False,
                "correct_option": "B",
                "concept": concept,
                "heading": "Let's look at this another way.",
                "subheading": "I noticed a small misunderstanding.",
                "student_answer": "Current increases",
                "teacher_observation": "The relationship between resistance and current appears reversed.",
                "misconception_category": "concept_reversal",
                "original_approach": "Formula: I = V / R",
                "new_approach": "Water-pipe analogy (narrow vs wide pipe)",
                "adapted_label": "Teacher adapted the lesson",
                "next_action": "Try a different explanation →",
                "next_state": TeachingState.REMEDIATE
            }

    def get_teacher_brain(self) -> Dict[str, Any]:
        return self.teacher_brain_state
