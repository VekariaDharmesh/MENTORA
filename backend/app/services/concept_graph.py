"""
Concept Graph & Prerequisite Knowledge Service
Maps concepts, prerequisite dependencies, and detects learning gaps.
"""

from typing import Dict, List, Any, Optional

class ConceptGraphService:
    def __init__(self):
        # Canonical Concept Graph for Electromagnetism & Physics
        self.concepts: Dict[str, Dict[str, Any]] = {
            "electric_charge": {
                "id": "c-01",
                "name": "Electric Charge",
                "domain": "Physics",
                "prerequisites": [],
                "difficulty": "beginner",
                "description": "Coulomb's Law, fundamental positive/negative charge carriers, and conservation of charge."
            },
            "electric_current": {
                "id": "c-02",
                "name": "Electric Current",
                "domain": "Physics",
                "prerequisites": ["electric_charge"],
                "difficulty": "beginner",
                "description": "Rate of flow of charge over time (I = Q / t). Amperes and electron drift velocity."
            },
            "voltage": {
                "id": "c-03",
                "name": "Voltage & Potential Difference",
                "domain": "Physics",
                "prerequisites": ["electric_charge"],
                "difficulty": "beginner",
                "description": "Work done per unit charge (ΔV = W / Q). Electric pressure that drives current."
            },
            "resistance": {
                "id": "c-04",
                "name": "Resistance & Impedance",
                "domain": "Physics",
                "prerequisites": ["electric_current"],
                "difficulty": "intermediate",
                "description": "Opposition to current flow caused by atomic collisions. Ohms (Ω) and dissipation."
            },
            "ohms_law": {
                "id": "c-05",
                "name": "Ohm's Law",
                "domain": "Physics",
                "prerequisites": ["voltage", "electric_current", "resistance"],
                "difficulty": "intermediate",
                "description": "Fundamental relationship V = I * R linking pressure, flow rate, and opposition."
            },
            "circuit_analysis": {
                "id": "c-06",
                "name": "Circuit Analysis & Kirchhoff's Laws",
                "domain": "Physics",
                "prerequisites": ["ohms_law"],
                "difficulty": "advanced",
                "description": "Series and parallel topologies, current division, and conservation of loop energy."
            }
        }

    def get_graph(self) -> Dict[str, Any]:
        """
        Returns full graph nodes and directed prerequisite edges.
        """
        nodes = []
        edges = []

        for key, data in self.concepts.items():
            nodes.append({
                "key": key,
                "id": data["id"],
                "name": data["name"],
                "domain": data["domain"],
                "difficulty": data["difficulty"],
                "description": data["description"]
            })
            for prereq in data["prerequisites"]:
                edges.append({
                    "from": prereq,
                    "to": key
                })

        return {
            "nodes": nodes,
            "edges": edges,
            "total_concepts": len(nodes)
        }

    def check_prerequisites(self, target_concept: str, student_mastery: Dict[str, float], threshold: float = 0.60) -> Dict[str, Any]:
        """
        Checks if the student satisfies all prerequisites before learning a target concept.
        """
        target = self.concepts.get(target_concept)
        if not target:
            return {"eligible": True, "missing_prerequisites": []}

        missing = []
        for prereq_key in target["prerequisites"]:
            score = student_mastery.get(prereq_key, 0.0)
            if score < threshold:
                missing.append({
                    "concept_key": prereq_key,
                    "concept_name": self.concepts[prereq_key]["name"],
                    "current_mastery": score,
                    "required_mastery": threshold
                })

        return {
            "eligible": len(missing) == 0,
            "target_concept": target["name"],
            "missing_prerequisites": missing
        }
