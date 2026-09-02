#!/usr/bin/env python3
"""
MENTORE — Automated End-to-End Terminal Demo
Demonstrates the full pedagogical cycle:
1. Ingest document & chunk
2. Query prerequisite concept graph
3. Generate dynamic lesson plan via LLM
4. Evaluate checkpoint: Misconception detection (Option A)
5. Adapt pedagogical strategy to Water-Pipe analogy
6. Re-evaluate student with correct answer (Option B)
7. Inspect real-time Teacher Brain state
8. Generate final diagnostic learning report
"""

import sys
import os
import json
import time

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.services.llm_service import LLMService
from app.services.concept_graph import ConceptGraphService
from app.teaching.state_machine import TeachingStateMachine
from app.services.learner_model import LearnerModelService
from app.services.assessment_engine import AssessmentEngineService
from app.services.visual_engine import VisualEngineService

def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

async def run_demo():
    print_header("AI TEACHER — CLOSED PEDAGOGICAL LOOP DEMO")
    time.sleep(0.5)

    # 1. Concept Graph & Prerequisites
    print("\n[Step 1] Loading Directed Concept Prerequisite Graph...")
    concept_service = ConceptGraphService()
    graph = concept_service.get_graph()
    print(f"  -> Total Concepts in Domain: {graph['total_concepts']}")
    for node in graph["nodes"]:
        print(f"     • [{node['id']}] {node['name']} ({node['difficulty']})")

    # 2. Dynamic Lesson Generation
    print_header("[Step 2] AI Lesson Planner: Generating Dynamic Curriculum")
    llm = LLMService()
    print("  -> Student Request: 'Teach me Understanding Electricity in 20 minutes in Hinglish'")
    plan = await llm.generate_lesson_plan("Understanding Electricity", "beginner", 20, "Hinglish")
    print(f"  -> Lesson Objective: {plan['objective']}")
    print(f"  -> Generated {len(plan['segments'])} structured learning segments:")
    for seg in plan["segments"]:
        ckpt_str = "[HAS CHECKPOINT]" if seg.get("has_checkpoint") else ""
        print(f"     Segment {seg['sequence']}: {seg['concept']} ({seg['duration']} min, {seg['strategy']}) {ckpt_str}")

    # 3. Checkpoint Evaluation: Option A (Misconception)
    print_header("[Step 3] Socratic Checkpoint: Student Answers Option A (Misconception)")
    print("  -> Question: 'What happens to the current in a circuit if resistance increases at constant voltage?'")
    print("  -> Student Answer: 'Option A (It increases proportionally)'")
    
    teaching = TeachingStateMachine()
    learner = LearnerModelService()
    
    result_a = teaching.evaluate_checkpoint("A", concept="Resistance")
    learner.update_mastery("resistance", is_correct=False)
    
    print("\n  -> AI EVALUATION RESULTS:")
    print(f"     • Correct: {result_a['is_correct']}")
    print(f"     • Diagnosed Misconception: {result_a['misconception_category']}")
    print(f"     • Pedagogical Decision: {result_a['next_state']}")
    print(f"     • New Approach: {result_a['new_approach']}")
    print(f"     • Teacher Feedback: {result_a['teacher_observation']}")

    # 4. Teacher Brain Inspection
    print_header("[Step 4] Transparent 'Teacher Brain' Real-Time Inspection")
    brain = teaching.get_teacher_brain()
    print(f"  -> Teacher Status:        {brain['status']}")
    print(f"  -> Active Concept:        {brain['current_concept']}")
    print(f"  -> Diagnosed Error:       {brain['detected_misconception']}")
    print(f"  -> Pedagogical Strategy:  {brain['strategy']}")
    print(f"  -> Pedagogical Reason:    {brain['reason']}")
    print(f"  -> Next Action:           {brain['next_action']}")

    # 5. Visual Engine Adaptation
    print_header("[Step 5] Dynamic Visual Engine: Switching to Water-Pipe Model")
    visual_service = VisualEngineService()
    pipe_res = visual_service.render_water_pipe_svg("Narrow")
    print(f"  -> Rendered Visual: {pipe_res['type'].upper()}")
    print(f"  -> Physical Model Description: {pipe_res['flow_description']}")
    print(f"  -> Generated SVG string length: {len(pipe_res['svg'])} characters")

    # 6. Re-Evaluation: Option B (Correct Equilibrium)
    print_header("[Step 6] Re-Evaluation: Student Corrects Misconception (Option B)")
    print("  -> Student Answer: 'Option B (It decreases inversely: I = V / R)'")
    result_b = teaching.evaluate_checkpoint("B", concept="Resistance")
    learner.update_mastery("resistance", is_correct=True)
    
    print("\n  -> AI EVALUATION RESULTS:")
    print(f"     • Correct: {result_b['is_correct']}")
    print(f"     • Next State: {result_b['next_state']}")
    print(f"     • Mastery Score: {result_b['mastery_before']}% -> {result_b['mastery_after']}% (+{result_b['mastery_after'] - result_b['mastery_before']}%)")
    print(f"     • Formula Equilibrium: {result_b['formula']}")

    # 7. Final Assessment & Editorial Report
    print_header("[Step 7] Diagnostic Quiz Evaluation & Learning Report")
    assessment_service = AssessmentEngineService()
    report = assessment_service.grade_assessment({"q1": "B", "q2": "A", "q3": "C", "q4": "B", "q5": "B", "q6": "C", "q7": "A", "q8": "B"})
    print(f"  -> Overall Score: {report['score_pct']}% ({report['correct_count']}/{report['total_questions']} correct)")
    print(f"  -> Strong Areas: {', '.join(report['strong_areas'])}")
    print(f"  -> Teacher Observations: {report['teacher_observation']}")
    print(f"  -> Recommended Next Path: {report['next_learning_step']}")

    print_header("DEMO COMPLETED SUCCESSFULLY — ALL ENGINES OPERATIONAL")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_demo())
