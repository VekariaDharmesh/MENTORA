/**
 * MENTORE — Unified JavaScript API Client SDK
 * Provides typed, asynchronous access to the MENTORE FastAPI backend with graceful fallbacks.
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const AITeacherAPI = {
  // System Health
  async checkHealth() {
    try {
      const res = await fetch('http://localhost:8000/health');
      return res.ok ? await res.json() : null;
    } catch {
      return null;
    }
  },

  // Knowledge Engine & Documents
  async listDocuments() {
    const res = await fetch(`${API_BASE_URL}/documents`);
    return await res.json();
  },

  async uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: 'POST',
      body: formData,
    });
    return await res.json();
  },

  // Concept Graph
  async getConceptGraph() {
    const res = await fetch(`${API_BASE_URL}/concepts/graph`);
    return await res.json();
  },

  // Student Learner Model
  async getKnowledgeState() {
    const res = await fetch(`${API_BASE_URL}/students/knowledge-state`);
    return await res.json();
  },

  // Teaching Engine & State Machine
  async submitCheckpointAnswer(choice, concept = 'Resistance') {
    const res = await fetch(`${API_BASE_URL}/teaching/checkpoint/answer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ choice, concept }),
    });
    return await res.json();
  },

  async inspectTeacherBrain() {
    const res = await fetch(`${API_BASE_URL}/teaching/brain-inspect`);
    return await res.json();
  },

  async askTeacher(question, concept = 'Resistance') {
    const res = await fetch(`${API_BASE_URL}/teaching/contextual-ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, concept }),
    });
    return await res.json();
  },

  // Visual Engine
  async renderVisual(params) {
    const res = await fetch(`${API_BASE_URL}/visuals/render`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    return await res.json();
  },

  // Multilingual Engine
  async switchLanguage(concept, targetLanguage) {
    const res = await fetch(`${API_BASE_URL}/teaching/language/switch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ concept, target_language: targetLanguage }),
    });
    return await res.json();
  },

  // Assessment & Learning Report
  async generateAssessment() {
    const res = await fetch(`${API_BASE_URL}/assessment/generate`);
    return await res.json();
  },

  async submitAssessment(studentAnswers) {
    const res = await fetch(`${API_BASE_URL}/assessment/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_answers: studentAnswers }),
    });
    return await res.json();
  },

  // Advanced Features
  async getFlashcards(topic = 'Electricity') {
    const res = await fetch(`${API_BASE_URL}/advanced/flashcards?topic=${encodeURIComponent(topic)}`);
    return await res.json();
  },

  async getStudyNotes(topic = 'Electricity') {
    const res = await fetch(`${API_BASE_URL}/advanced/notes?topic=${encodeURIComponent(topic)}`);
    return await res.json();
  },

  async startRevision(topic = "Ohm's Law") {
    const res = await fetch(`${API_BASE_URL}/advanced/revision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic }),
    });
    return await res.json();
  },

  // Telemetry & Accessibility
  async logAnalytics(eventType, metadata = {}) {
    try {
      await fetch(`${API_BASE_URL}/analytics/log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: 'demo_session',
          event_type: eventType,
          metadata,
        }),
      });
    } catch {}
  },
};
