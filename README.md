# AI Teacher — Warm Study Desk Educational Platform

> **A Cognitive AI Educator with Deterministic Pedagogical State Machine, Directed Prerequisite Concept Graphs, Bayesian Learner Mastery Modeling, and Real-Time Adaptive Misconception Remediation.**

---

## 🌟 The Core Philosophy: "Warm Study Desk"
Education should feel like sitting at a calm, sunlit physical wooden study desk with a patient academic mentor — not a noisy, neon SaaS dashboard. 

The AI Teacher avoids generic AI chatbots. Instead, it utilizes a **multi-engine cognitive architecture**:
$$\text{\bfseries LLM} \;+\; \text{\bfseries Pedagogical State Machine} \;+\; \text{\bfseries Concept Graph RAG} \;+\; \text{\bfseries Bayesian Learner Model} \;+\; \text{\bfseries Dynamic Media Engine}$$

---

## 🔄 The Closed Pedagogical Loop
$$\text{\bfseries Understand} \longrightarrow \text{\bfseries Plan} \longrightarrow \text{\bfseries Explain} \longrightarrow \text{\bfseries Demonstrate} \longrightarrow \text{\bfseries Question} \longrightarrow \text{\bfseries Evaluate} \longrightarrow \text{\bfseries Adapt} \longrightarrow \text{\bfseries Continue}$$

1. **Understand**: Documents (PDF, DOCX, TXT) are parsed via PyMuPDF into semantic 400-word chunks and linked to a directed concept graph.
2. **Plan**: LLM curriculum generator builds a personalized 4-5 segment lesson tailored to student level and time constraint.
3. **Explain**: Dr. Aris (vector SVG animated teacher) articulates concepts with synchronized speech synthesis in Hinglish, Hindi, or English.
4. **Demonstrate**: Subject-aware dynamic SVG visual stage calculates physical equations in real time ($I = V / R$).
5. **Question**: Conceptual checkpoints test student physical intuition.
6. **Evaluate**: Instant classification into correct equilibrium or diagnosed misconception (`concept_reversal`).
7. **Adapt**: Automatic remediation switching to the tactile **Water-Pipe Analogy** with real-time **Teacher Brain** transparency.
8. **Continue**: 8-question diagnostic assessment, editorial learning report, and targeted 5-minute revision sprint.

---

## 🏛️ Multi-Tier Clean Architecture

```text
├── frontend/             # Tier 1: Client UI, Animated Character Dr. Aris, CSS Design System
├── backend/              # Tier 2: FastAPI Cognitive Pedagogical Engine & Domain Services
├── database/             # Tier 3: PostgreSQL + pgvector DDL, Seeds, and Init Script
├── api/                  # Tier 4: OpenAPI 3.1 Spec & Reusable Async JavaScript SDK
├── Dockerfile            # Production Python 3.11-slim container
└── docker-compose.yml    # Multi-container stack (Backend, Postgres, Redis, Nginx)
```

---

## 🚀 Quick Start Guide

### 1. Run via Local Development (Zero Docker Needed)

#### Backend:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000 --reload
```
Interactive Swagger API documentation: **[http://localhost:8000/docs](http://localhost:8000/docs)**

#### Frontend:
```bash
python3 -m http.server 3000
```
Open **[http://localhost:3000/](http://localhost:3000/)** in your browser.

---

### 2. Run Automated End-to-End Test Suite (11/11 Passing)
```bash
python3 backend/tests/test_api.py
```

---

### 3. Run Automated CLI Demo
```bash
python3 demo.py
```

---

### 4. Run via Docker Compose (Full Stack)
```bash
docker-compose up --build
```
- Frontend UI: `http://localhost:3000`
- FastAPI Engine: `http://localhost:8000`
- PostgreSQL + pgvector: `localhost:5432`
- Redis Cache: `localhost:6379`

---

## 🧠 Key Features for Hackathon Judges

1. **Living Vector Animated Character (Dr. Aris)**:
   - 60fps micro-animations: breathing chest, contemplative head tilt, randomized eye blinks, and gaze shifts.
   - Mouth articulation automatically synchronizes to spoken audio and speech synthesis.
2. **Transparent "Teacher Brain" Drawer**:
   - Slide-out educator inspector revealing internal pedagogical parameters in real time (mastery score, detected misconception, confidence level, strategy, and next pedagogical action).
3. **Adaptive Misconception Branching**:
   - Option B (Correct, $I = V / R$): Advances mastery to $78\%$.
   - Option A (Misconception, "Current increases with resistance"): Diagnoses `concept_reversal` and triggers hydraulic water-pipe constriction demonstration.
4. **Multilingual Context Switching**:
   - Live switching across Hinglish, Hindi, and English without losing session history or mastery progress.
