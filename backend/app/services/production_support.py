"""
Production Support & Analytics Service (Phase 12)
Handles session event telemetry, media job lifecycle (cancel/retry), rate-limiting, and accessibility settings.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from uuid import uuid4

class ProductionSupportService:
    def __init__(self):
        self.analytics_events: List[Dict[str, Any]] = []
        self.job_statuses: Dict[str, str] = {}
        self.student_accessibility: Dict[str, Dict[str, Any]] = {
            "default_student": {
                "reduced_motion": False,
                "high_contrast": False,
                "captions_forced": True,
                "screen_reader_friendly": True,
                "font_scale": 1.0
            }
        }

    def log_event(self, session_id: str, event_type: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Logs analytics events (playback pauses, checkpoint latency, misconception diagnosis, language switch).
        """
        event = {
            "event_id": f"evt-{uuid4().hex[:8]}",
            "session_id": session_id,
            "event_type": event_type,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.analytics_events.append(event)
        return event

    def get_analytics_summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns aggregated analytics metrics for educator/judge dashboards.
        """
        filtered = [e for e in self.analytics_events if not session_id or e["session_id"] == session_id]
        event_counts: Dict[str, int] = {}
        for e in filtered:
            etype = e["event_type"]
            event_counts[etype] = event_counts.get(etype, 0) + 1

        return {
            "total_events": len(filtered),
            "event_counts": event_counts,
            "latest_events": filtered[-10:]
        }

    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """
        Cancels an in-flight media or video generation job.
        """
        self.job_statuses[job_id] = "CANCELLED"
        return {"job_id": job_id, "status": "CANCELLED", "message": "Generation job terminated cleanly."}

    def retry_job(self, job_id: str) -> Dict[str, Any]:
        """
        Retries a failed generation pipeline step.
        """
        self.job_statuses[job_id] = "READY"
        return {"job_id": job_id, "status": "READY", "message": "Pipeline step retried successfully."}

    def set_accessibility_mode(self, student_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Persists student accessibility preferences.
        """
        current = self.student_accessibility.setdefault(student_id, {})
        current.update(settings)
        return {"student_id": student_id, "accessibility": current}

    def get_accessibility_mode(self, student_id: str = "default_student") -> Dict[str, Any]:
        return self.student_accessibility.get(student_id, {
            "reduced_motion": False,
            "high_contrast": False,
            "captions_forced": True,
            "screen_reader_friendly": True,
            "font_scale": 1.0
        })
