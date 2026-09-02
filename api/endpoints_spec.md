# MENTORE — REST API Specification (V1)

**Base URL**: `http://localhost:8000/api/v1`  
**OpenAPI Specification**: [`api/openapi.json`](file:///Users/vekariadharmeshh/Movies/SSSV/api/openapi.json)  
**Interactive Swagger UI**: `http://localhost:8000/docs`  
**Interactive ReDoc**: `http://localhost:8000/redoc`

---

## 1. System Endpoints

### `GET /health`
Confirms the pedagogical engine status.

**Response**:
```json
{
  "status": "healthy",
  "engine": "MENTORE Pedagogical Engine",
  "mode": "Socratic Adaptive Mode",
  "version": "1.0.0"
}
```

---

## 2. Knowledge Engine & Documents

### `POST /api/v1/documents/upload`
Uploads a document (PDF, DOCX, TXT), runs semantic chunking, and detects chapters.

### `GET /api/v1/documents`
Lists all documents in the student's material library.

---

## 3. Concept Graph

### `GET /api/v1/concepts/graph`
Returns directed prerequisite dependencies between domain concepts.

**Response Nodes**:
- `electric_charge` (Beginner)
- `electric_current` (Beginner)
- `voltage` (Beginner)
- `resistance` (Intermediate)
- `ohms_law` (Intermediate)
- `circuit_analysis` (Advanced)

---

## 4. Student Learner Model

### `GET /api/v1/students/knowledge-state`
Returns the student's real-time Bayesian mastery scores and active misconceptions.

---

## 5. Lesson Planner

### `POST /api/v1/lessons/create`
Generates a structured multi-segment lesson plan.

**Payload**:
```json
{
  "topic": "Understanding Electricity",
  "level": "beginner",
  "duration_minutes": 20,
  "language": "Hinglish",
  "objective": "Understand Ohm's Law and Circuit Flow"
}
```

---

## 6. Teaching Engine & State Machine

### `POST /api/v1/teaching/checkpoint/answer`
Evaluates student response, updating mastery or triggering adaptive remediation.

**Payload**:
```json
{
  "choice": "A",
  "concept": "Resistance"
}
```

**Adaptive Response (`choice: A` — Misconception)**:
```json
{
  "is_correct": false,
  "misconception_category": "concept_reversal",
  "new_approach": "Water-pipe analogy (narrow vs wide pipe)",
  "next_state": "REMEDIATE"
}
```

### `GET /api/v1/teaching/brain-inspect`
Returns real-time cognitive educator parameters for the transparent side inspector.

### `POST /api/v1/teaching/contextual-ask`
Contextual Q&A grounded in the active lesson concept.

---

## 7. Subject-Aware Visuals

### `POST /api/v1/visuals/render`
Renders dynamic electrical circuit or hydraulic water-pipe SVG visuals.

**Payload**:
```json
{
  "visual_type": "circuit",
  "voltage": 9.0,
  "resistance": 15.0,
  "switch_closed": true
}
```

---

## 8. Multilingual Engine

### `POST /api/v1/teaching/language/switch`
Translates concept explanations across Hinglish, Hindi, and English.

**Payload**:
```json
{
  "concept": "voltage",
  "target_language": "Hindi"
}
```

---

## 9. Media & Voice Synthesis

### `POST /api/v1/media/voice/synthesize`
Generates audio voice segments with tracking and URLs.

### `POST /api/v1/media/fallback`
Triggers graceful degradation to audio + visual canvas + captions if video pipelines fail.

---

## 10. Assessment & Learning Report

### `GET /api/v1/assessment/generate`
Generates an 8-question concept-aligned diagnostic quiz.

### `POST /api/v1/assessment/submit`
Evaluates student quiz answers and returns score, strong areas, needs practice, and teacher notes.

---

## 11. Advanced Features

### `GET /api/v1/advanced/flashcards`
Returns active recall Socratic flashcards.

### `GET /api/v1/advanced/notes`
Returns Cornell-style study notes.

### `POST /api/v1/advanced/homework`
Generates targeted practice problem sets based on weak areas.

### `POST /api/v1/advanced/revision`
Initializes a 5-minute targeted revision sprint.

---

## 12. Production Telemetry & Accessibility

### `POST /api/v1/analytics/log`
Logs session telemetry and pedagogical events.

### `GET /api/v1/analytics/summary`
Returns aggregated event counts and recent logs.

### `POST /api/v1/accessibility/mode`
Persists student accessibility preferences.
