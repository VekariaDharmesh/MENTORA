"""
Student Knowledge State & Learner Model Service
Maintains weighted concept mastery scores, tracks confidence, and logs diagnosed misconceptions.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

class LearnerModelService:
    def __init__(self, student_id: str = "default_student"):
        self.student_id = student_id
        # In-memory session store (connects to PostgreSQL in production)
        self.concept_mastery: Dict[str, Dict[str, Any]] = {
            "electric_charge": {"score": 0.98, "confidence": 0.95, "attempts": 6, "correct": 6},
            "electric_current": {"score": 0.91, "confidence": 0.88, "attempts": 5, "correct": 4},
            "voltage": {"score": 0.84, "confidence": 0.82, "attempts": 4, "correct": 3},
            "resistance": {"score": 0.42, "confidence": 0.37, "attempts": 4, "correct": 2},
            "ohms_law": {"score": 0.38, "confidence": 0.30, "attempts": 2, "correct": 1},
        }
        self.misconceptions: List[Dict[str, Any]] = [
            {
                "id": "misc-01",
                "concept": "resistance",
                "category": "concept_reversal",
                "detected_statement": "Current increases when resistance increases",
                "teacher_observation": "The relationship between resistance and current appears reversed.",
                "resolved": False,
                "timestamp": datetime.utcnow().isoformat()
            }
        ]

    def get_knowledge_state(self) -> Dict[str, Any]:
        """
        Returns full student profile, concept mastery percentages, and active misconceptions.
        """
        return {
            "student_id": self.student_id,
            "concepts": {
                k: {
                    "mastery_score": round(v["score"], 2),
                    "mastery_pct": int(v["score"] * 100),
                    "confidence_score": round(v["confidence"], 2),
                    "attempts": v["attempts"],
                    "correct": v["correct"]
                }
                for k, v in self.concept_mastery.items()
            },
            "active_misconceptions": [m for m in self.misconceptions if not m["resolved"]],
            "total_mastered": len([v for v in self.concept_mastery.values() if v["score"] >= 0.80])
        }

    def update_mastery(self, concept_key: str, is_correct: bool, confidence_weight: float = 0.85) -> Dict[str, Any]:
        """
        Applies weighted Bayesian-style mastery update following a checkpoint attempt.
        """
        if concept_key not in self.concept_mastery:
            self.concept_mastery[concept_key] = {"score": 0.50, "confidence": 0.50, "attempts": 0, "correct": 0}

        entry = self.concept_mastery[concept_key]
        entry["attempts"] += 1

        delta = 0.10 * confidence_weight if is_correct else -0.08
        if is_correct:
            entry["correct"] += 1
            entry["score"] = min(1.0, entry["score"] + delta)
            entry["confidence"] = min(1.0, entry["confidence"] + 0.05)
        else:
            entry["score"] = max(0.0, entry["score"] + delta)
            entry["confidence"] = max(0.1, entry["confidence"] - 0.05)

        return {
            "concept": concept_key,
            "updated_score": round(entry["score"], 2),
            "updated_pct": int(entry["score"] * 100),
            "is_correct": is_correct
        }

    def record_misconception(self, concept_key: str, category: str, student_answer: str, observation: str) -> Dict[str, Any]:
        """
        Logs a diagnosed misconception into the learner model.
        """
        record = {
            "id": f"misc-{len(self.misconceptions) + 1:02d}",
            "concept": concept_key,
            "category": category,
            "detected_statement": student_answer,
            "teacher_observation": observation,
            "resolved": False,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.misconceptions.append(record)
        return record

    def resolve_misconception(self, misconception_id: str) -> bool:
        for m in self.misconceptions:
            if m["id"] == misconception_id:
                m["resolved"] = True
                m["resolved_at"] = datetime.utcnow().isoformat()
                return True
        return False
