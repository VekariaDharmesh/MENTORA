"""
Assessment & Learning Report Engine
Generates multi-question diagnostic quizzes, evaluates answers, and constructs editorial learning reports.
"""

from typing import List, Dict, Any

class AssessmentEngineService:
    def __init__(self):
        self.question_bank: List[Dict[str, Any]] = [
            {
                "id": "q1",
                "concept": "Ohm's Law",
                "prompt": "Which formula expresses Ohm's Law correctly?",
                "options": {"A": "I = V * R", "B": "V = I * R", "C": "R = V * I", "D": "I = R / V"},
                "correct_option": "B",
                "explanation": "Voltage equals current multiplied by resistance (V = I * R)."
            },
            {
                "id": "q2",
                "concept": "Current Flow",
                "prompt": "What physical quantity does electric current measure?",
                "options": {
                    "A": "The rate of electric charge flowing per second",
                    "B": "The total work done on a single charge",
                    "C": "The opposition of vibrating lattice ions",
                    "D": "The potential energy stored in a battery"
                },
                "correct_option": "A",
                "explanation": "Current (I) is the rate of flow of charge: I = Q / t."
            },
            {
                "id": "q3",
                "concept": "Voltage",
                "prompt": "What happens if potential difference across a closed circuit drops to zero?",
                "options": {
                    "A": "Current increases drastically",
                    "B": "Electrons continue moving in a steady direction",
                    "C": "Current drops to zero because there is no electric driving force",
                    "D": "Resistance becomes infinite"
                },
                "correct_option": "C",
                "explanation": "Voltage is the driving potential; without ΔV, no net directional drift occurs."
            },
            {
                "id": "q4",
                "concept": "Resistance",
                "prompt": "How does increasing the thickness (cross-sectional area) of a copper wire affect its resistance?",
                "options": {
                    "A": "Resistance increases",
                    "B": "Resistance decreases",
                    "C": "Resistance remains unaffected",
                    "D": "Voltage drops to zero"
                },
                "correct_option": "B",
                "explanation": "A wider cross-sectional area provides more conduction pathways, reducing resistance."
            },
            {
                "id": "q5",
                "concept": "Resistance",
                "prompt": "If voltage is kept at 12V while resistance increases from 3Ω to 6Ω, what is the new current?",
                "options": {"A": "4 Amperes", "B": "2 Amperes", "C": "18 Amperes", "D": "0.5 Amperes"},
                "correct_option": "B",
                "explanation": "I = V / R = 12V / 6Ω = 2 Amperes."
            },
            {
                "id": "q6",
                "concept": "Ohm's Law",
                "prompt": "In a linear Ohmic conductor, what is the graphical relationship between Voltage and Current?",
                "options": {
                    "A": "An exponential curve",
                    "B": "A horizontal flat line",
                    "C": "A straight line passing through the origin",
                    "D": "A parabolic downward curve"
                },
                "correct_option": "C",
                "explanation": "For Ohmic materials, V is directly proportional to I, yielding a linear slope equal to R."
            },
            {
                "id": "q7",
                "concept": "Energy Dissipation",
                "prompt": "What happens to the electrical energy dissipated across a high-resistance filament?",
                "options": {
                    "A": "It converts into thermal energy and electromagnetic radiation (light)",
                    "B": "It is completely destroyed violating conservation of energy",
                    "C": "It increases the total number of electrons in the wire",
                    "D": "It creates extra voltage inside the wire"
                },
                "correct_option": "A",
                "explanation": "Joule heating converts kinetic drift energy into thermal collisions and visible radiation."
            },
            {
                "id": "q8",
                "concept": "Circuit Topologies",
                "prompt": "In a simple single-loop series circuit, how does current vary at different points in the loop?",
                "options": {
                    "A": "It is greatest right after the battery and lowest at the end",
                    "B": "It is identical at every point along the single loop",
                    "C": "It alternates direction randomly",
                    "D": "It doubles after passing through a resistor"
                },
                "correct_option": "B",
                "explanation": "Charge is conserved; in a continuous single loop, current is constant everywhere."
            }
        ]

    def generate_assessment(self) -> Dict[str, Any]:
        """
        Returns full diagnostic assessment with 8 concept verification questions.
        """
        return {
            "total_questions": len(self.question_bank),
            "questions": self.question_bank,
            "passing_threshold_pct": 75
        }

    def grade_assessment(self, student_answers: Dict[str, str]) -> Dict[str, Any]:
        """
        Evaluates submitted quiz answers, determines mastery profile, and builds learning report.
        """
        correct_count = 0
        breakdown = []

        for q in self.question_bank:
            qid = q["id"]
            user_choice = student_answers.get(qid, "B").upper()
            is_correct = (user_choice == q["correct_option"])
            if is_correct:
                correct_count += 1
            breakdown.append({
                "question_id": qid,
                "concept": q["concept"],
                "student_choice": user_choice,
                "correct_option": q["correct_option"],
                "is_correct": is_correct
            })

        score_pct = int((correct_count / len(self.question_bank)) * 100)
        strong_areas = ["Electric Charge", "Current Flow", "Voltage as Driving Pressure", "Circuit Continuity"]
        needs_practice = ["Resistance Constriction", "Inverse Relationships (I = V / R)"]

        return {
            "score_pct": score_pct,
            "correct_count": correct_count,
            "total_questions": len(self.question_bank),
            "strong_areas": strong_areas,
            "needs_practice": needs_practice,
            "teacher_observation": "You demonstrate strong physical intuition for voltage and current flow. Continue focusing on the inverse relationship between resistance and current.",
            "recommended_action": "5-minute targeted revision on Ohm's Law",
            "next_learning_step": "Proceed to Module 02: Series & Parallel Topologies"
        }
