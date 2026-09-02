# MENTORE — Warm Study Desk Educational Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-00a393.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A Cognitive AI Educator with a Deterministic Pedagogical State Machine, Directed Prerequisite Concept Graphs, Bayesian Learner Mastery Modeling, and Real-Time Adaptive Misconception Remediation.**

## 🌟 The Core Philosophy: "Warm Study Desk"
Education should feel like sitting at a calm, sunlit physical wooden study desk with a patient academic mentor — not a noisy, neon SaaS dashboard. 

The **MENTORE** avoids generic AI chatbots. Instead, it utilizes a **multi-engine cognitive architecture**:
$$\text{\bfseries LLM} \;+\; \text{\bfseries Pedagogical State Machine} \;+\; \text{\bfseries Concept Graph RAG} \;+\; \text{\bfseries Bayesian Learner Model} \;+\; \text{\bfseries Dynamic Media Engine}$$

---

## 📽️ Asynchronous Video Generation Pipeline
Unlike traditional mock-ups, this platform dynamically generates educational videos based on the student's curriculum and adaptations. 

The pipeline handles:
1. **Script Generation**: Powered by the LLM.
2. **Text-to-Speech (TTS)**: Translates the script into natural, multilingual speech (e.g., ElevenLabs / OpenAI).
3. **Visual Planning**: Generates SVG diagrams, circuits, or math equations on the fly.
4. **Avatar Engine**: Connects to avatar APIs (e.g., HeyGen) to synthesize the teacher's video.
5. **FFmpeg Composition**: The background worker composites the audio, visuals, and avatar video.
6. **Graceful Fallback**: If external API keys are missing or generation fails, it seamlessly degrades to audio-only explanations with visual canvasses without breaking the lesson loop.

---

## 🔄 The Closed Pedagogical Loop
$$\text{\bfseries Understand} \longrightarrow \text{\bfseries Plan} \longrightarrow \text{\bfseries Explain} \longrightarrow \text{\bfseries Demonstrate} \longrightarrow \text{\bfseries Question} \longrightarrow \text{\bfseries Evaluate} \longrightarrow \text{\bfseries Adapt} \longrightarrow \text{\bfseries Continue}$$

1. **Understand**: Documents (PDF, DOCX, TXT) are parsed via PyMuPDF into semantic 400-word chunks and linked to a directed concept graph.
2. **Plan**: LLM curriculum generator builds a personalized 4-5 segment lesson tailored to student level and time constraints.
3. **Explain**: Dr. Aris (vector SVG animated teacher) articulates concepts with synchronized speech synthesis in Hinglish, Hindi, or English.
4. **Demonstrate**: Subject-aware dynamic SVG visual stage calculates physical equations in real time ($I = V / R$).
5. **Question**: Conceptual checkpoints test student physical intuition.
6. **Evaluate**: Instant classification into correct equilibrium or diagnosed misconception (`concept_reversal`).
7. **Adapt**: Automatic remediation switching to the tactile **Water-Pipe Analogy** with real-time **Teacher Brain** transparency.
8. **Continue**: 8-question diagnostic assessment, editorial learning report, and targeted 5-minute revision sprint.

---

## 🏛️ Clean Architecture

```text
├── frontend/             # Tier 1: Client UI, Animated Character Dr. Aris, CSS Design System
├── backend/              # Tier 2: FastAPI Cognitive Pedagogical Engine, Media Engine & Domain Services
├── database/             # Tier 3: PostgreSQL + pgvector DDL, Seeds, and Init Script
├── api/                  # Tier 4: OpenAPI 3.1 Spec & Reusable Async JavaScript SDK
├── Dockerfile            # Production Python 3.11-slim container
└── docker-compose.yml    # Multi-container stack (Backend, Postgres, Redis, Nginx)
```

---

## ⚙️ Prerequisites
- **Python 3.11+**
- **FFmpeg**: Required for the background video composition pipeline. 
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
- **Docker & Docker Compose** (Optional, for full stack deployment)

---

## 🚀 Quick Start Guide

### 1. Environment Setup
Copy the example environment file and configure your API keys for the media pipeline to fully function:
```bash
cp backend/.env.example backend/.env
```
Ensure you add your actual `GEMINI_API_KEY`, `TTS_API_KEY`, and `AVATAR_API_KEY`. If left empty or as placeholders, the pipeline gracefully falls back to the audio-visual UI.

### 2. Run via Local Development (Zero Docker Needed)

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000 --reload
```
Interactive API documentation: **[http://localhost:8000/docs](http://localhost:8000/docs)**

**Frontend:**
```bash
# In the root directory (or frontend/ directory)
python3 -m http.server 3000
```
Open **[http://localhost:3000/](http://localhost:3000/)** in your browser.

---

### 3. Run Automated CLI Demo & Tests
```bash
# Run End-to-End Test Suite (11/11 Passing)
python3 backend/tests/test_api.py

# Run Automated CLI Demo
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
5. **Real-time Video Pipeline Polling**:
   - Background API jobs composite the generated lesson with FFmpeg, actively updating the UI until the customized video is deployed to the lesson player.

