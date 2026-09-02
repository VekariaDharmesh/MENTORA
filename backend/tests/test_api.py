"""
Automated Test Suite for MENTORE API
Tests the complete pedagogical pipeline:
- System Health
- Concept Graph & Prerequisites
- Dynamic LLM Lesson Planner
- Socratic Checkpoint Evaluation (Equilibrium vs Misconception)
- Subject-Aware Visual Rendering
- Multilingual Context Switching
- Final Assessment & Report Generation
- Advanced Features (Flashcards, Notes, Revision)
- Production Telemetry
"""

import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Pedagogical" in data["engine"]

def test_concept_graph():
    response = client.get("/api/v1/concepts/graph")
    assert response.status_code == 200
    data = response.json()
    assert data["total_concepts"] >= 6
    assert any(n["key"] == "ohms_law" for n in data["nodes"])

def test_lesson_creation():
    payload = {
        "topic": "Understanding Electricity",
        "level": "beginner",
        "duration_minutes": 20,
        "language": "Hinglish"
    }
    response = client.post("/api/v1/lessons/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Understanding Electricity"
    assert len(data["segments"]) >= 4
    assert "lesson_id" in data

def test_checkpoint_evaluation_correct():
    # Option B = Correct ("It decreases")
    payload = {"choice": "B", "concept": "Resistance"}
    response = client.post("/api/v1/teaching/checkpoint/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["next_state"] == "ADVANCE"
    assert data["mastery_after"] == 78

def test_checkpoint_evaluation_misconception():
    # Option A = Misconception ("It increases")
    payload = {"choice": "A", "concept": "Resistance"}
    response = client.post("/api/v1/teaching/checkpoint/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    assert data["misconception_category"] == "concept_reversal"
    assert "water-pipe" in data["new_approach"].lower()
    assert data["next_state"] == "REMEDIATE"

def test_teacher_brain_inspector():
    response = client.get("/api/v1/teaching/brain-inspect")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "decision" in data
    assert "current_concept" in data

def test_visual_rendering():
    payload = {"visual_type": "circuit", "voltage": 9.0, "resistance": 15.0, "switch_closed": True}
    response = client.post("/api/v1/visuals/render", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["current"] == 0.6
    assert "<svg" in data["svg"]

def test_multilingual_translation():
    payload = {"concept": "voltage", "target_language": "Hindi"}
    response = client.post("/api/v1/teaching/language/switch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "वोल्टेज" in data["title"]

def test_assessment_generation_and_submission():
    gen_res = client.get("/api/v1/assessment/generate")
    assert gen_res.status_code == 200
    assert gen_res.json()["total_questions"] == 8

    sub_res = client.post("/api/v1/assessment/submit", json={"student_answers": {"q1": "B", "q2": "A"}})
    assert sub_res.status_code == 200
    data = sub_res.json()
    assert "score_pct" in data
    assert len(data["strong_areas"]) > 0

def test_advanced_features():
    fc_res = client.get("/api/v1/advanced/flashcards?topic=Electricity")
    assert fc_res.status_code == 200
    assert len(fc_res.json()["flashcards"]) >= 4

    notes_res = client.get("/api/v1/advanced/notes?topic=Electricity")
    assert notes_res.status_code == 200
    assert "cue_column" in notes_res.json()

    rev_res = client.post("/api/v1/advanced/revision", json={"topic": "Ohm's Law"})
    assert rev_res.status_code == 200
    assert rev_res.json()["target_duration_minutes"] == 5

def test_production_telemetry():
    log_res = client.post("/api/v1/analytics/log", json={
        "session_id": "test_session",
        "event_type": "checkpoint_answered",
        "metadata": {"score": 100}
    })
    assert log_res.status_code == 200

    sum_res = client.get("/api/v1/analytics/summary")
    assert sum_res.status_code == 200
    assert sum_res.json()["total_events"] >= 1

def test_teaching_websocket():
    with client.websocket_connect("/api/v1/ws/lesson/sess-test-01") as websocket:
        init_data = websocket.receive_json()
        assert init_data["type"] == "SESSION_INIT"
        assert init_data["teacher"] == "Dr. Aris"

        websocket.send_json({"type": "PING"})
        pong_data = websocket.receive_json()
        assert pong_data["type"] == "PONG"

if __name__ == "__main__":
    tests = [
        test_health_check,
        test_concept_graph,
        test_lesson_creation,
        test_checkpoint_evaluation_correct,
        test_checkpoint_evaluation_misconception,
        test_teacher_brain_inspector,
        test_visual_rendering,
        test_multilingual_translation,
        test_assessment_generation_and_submission,
        test_advanced_features,
        test_production_telemetry,
        test_teaching_websocket
    ]
    passed = 0
    print(f"\n[MENTORE Test Suite] Running {len(tests)} automated tests...")
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  ✓ {t.__name__} PASSED")
        except Exception as e:
            print(f"  ✗ {t.__name__} FAILED: {e}")

    print(f"\n[MENTORE Test Suite] Results: {passed}/{len(tests)} tests passed successfully!\n")
    if passed == len(tests):
        sys.exit(0)
    else:
        sys.exit(1)
