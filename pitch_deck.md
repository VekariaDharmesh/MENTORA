# MENTORE — Pitch Deck & Judge Presentation Guide

## 1. The Core Problem
1. **Passive Video Watching**: 92% of students drop out of online courses because pre-recorded videos cannot pause, detect confusion, or answer questions.
2. **Generic Chatbots Are Poor Educators**: Raw LLMs (ChatGPT) will dump 10 paragraphs of text or answers without diagnosing underlying cognitive misconceptions or following structured pedagogy.
3. **No Socratic Adaptation**: Existing platforms follow linear curriculum. If a student reverses a concept (e.g., believing resistance increases current), the system blindly marches forward.

---

## 2. Our Solution: The "Warm Study Desk" MENTORE
A calm, distraction-free digital study desk with a patient, living academic mentor (Dr. Aris).

Instead of treating the LLM as the entire backend, we built a **technically defensible cognitive engine**:
$$\text{\bfseries LLM} \;+\; \text{\bfseries Deterministic State Machine} \;+\; \text{\bfseries Directed Concept Graph} \;+\; \text{\bfseries Bayesian Learner Model} \;+\; \text{\bfseries Subject-Aware Visuals}$$

---

## 3. The 3-Minute Live Demo Script (For Judges)

### Minute 1: The First Impression & Persona
- **Screen**: Landing / Onboarding (`http://localhost:3000/#landing`).
- **Showcase**:
  - The "Warm Study Desk" aesthetic: ivory matte parchment, terracotta, moss green, and dark charcoal typography.
  - The living vector teacher character **Dr. Aris**: 60fps breathing chest, thoughtful head tilt, randomized natural eye blinks, and gaze shifts.

### Minute 2: The Socratic Loop & Misconception Adaptation (The WOW Moment)
- **Screen**: Lesson Player (`#view-player`).
- **Showcase**:
  - Notice the dynamic circuit diagram on the visual stage calculating $I = V / R$.
  - Click **⚡ Quick Check** to trigger the conceptual checkpoint:
    > *"What happens to current if resistance increases at constant voltage?"*
  - **Deliberately choose Option A ("It increases proportionally")**.
  - **The Adaptation**:
    - Dr. Aris detects the misconception: `concept_reversal`.
    - Opens the **Teacher Brain** inspector to prove real-time decision-making (`RE-EXPLAIN`, strategy: `Water-pipe analogy`).
    - The visual canvas instantly transforms from an electrical circuit to a **hydraulic water pipe with a narrow constriction**, teaching the concept intuitively!

### Minute 3: Re-Evaluation & Mastery Growth
- **Showcase**:
  - Re-evaluate with **Option B ("It decreases inversely: I = V / R")**.
  - Student mastery jumps from $68\%$ to $78\%$.
  - Click the **Language Switcher** button: Watch Dr. Aris seamlessly switch between **Hinglish**, **Hindi**, and **English** with real-time speech narration without resetting lesson state.
  - Complete the 8-question assessment to generate the editorial **Learning Report** and trigger the 5-minute **Revision Sprint**.

---

## 4. Technical Architecture
```text
┌─────────────────────────────────────────────────────────────┐
│                    Warm Study Desk Client                   │
│        (HTML / CSS Design System / Native Web Speech)       │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST / JSON (api/client.js)
┌──────────────────────────────▼──────────────────────────────┐
│                  FastAPI Cognitive Gateway                  │
│   (Clean Architecture: schemas, core, services, api/v1)     │
└───────┬──────────────────────┬──────────────────────┬───────┘
        │                      │                      │
┌───────▼──────┐       ┌───────▼──────┐       ┌───────▼──────┐
│  LLM Service │       │ State Machine│       │Learner Model │
│(Curriculum / │       │(Pedagogical  │       │  (Bayesian   │
│ Misconception│       │    Loop)     │       │   Mastery)   │
└───────┬──────┘       └───────┬──────┘       └───────┬──────┘
        │                      │                      │
┌───────▼──────────────────────▼──────────────────────▼───────┐
│                 PostgreSQL + pgvector Database              │
│       (6-node directed concept graph & prerequisite RAG)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Why We Win
- **Pedagogically Grounded**: We implemented the full loop: *Understand $\rightarrow$ Plan $\rightarrow$ Explain $\rightarrow$ Demonstrate $\rightarrow$ Question $\rightarrow$ Evaluate $\rightarrow$ Adapt $\rightarrow$ Continue*.
- **No Test/Mock Data**: Driven entirely by live backend APIs and dynamic LLM planning.
- **Enterprise Grade**: 11/11 automated tests passing, Dockerized, and integrated with GitHub Actions CI/CD.
