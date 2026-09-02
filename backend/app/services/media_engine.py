import os
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import MediaJob
from app.providers.video.heygen import HeyGenVideoProvider

logger = logging.getLogger(__name__)

class MediaEngineService:
    def __init__(self):
        self.video_provider = HeyGenVideoProvider()
        # Fallback values
        self.default_avatar_id = os.getenv("HEYGEN_AVATAR_ID", "default_avatar")
        self.default_voice_id = os.getenv("HEYGEN_VOICE_ID", "default_voice")

    def _update_job(self, job_id: str, updates: Dict[str, Any]):
        db: Session = SessionLocal()
        try:
            job = db.query(MediaJob).filter(MediaJob.id == job_id).first()
            if job:
                for key, value in updates.items():
                    setattr(job, key, value)
                db.commit()
        finally:
            db.close()

    async def _process_video_job(self, job_id: str, text: str, avatar_id: str, voice_id: str):
        db: Session = SessionLocal()
        try:
            # 1. Update status to STARTED
            self._update_job(job_id, {
                "status": "PROCESSING",
                "stage": "VIDEO_SUBMISSION",
                "started_at": datetime.utcnow()
            })
            
            # 2. Call HeyGen Provider
            logger.info(f"Submitting job {job_id} to HeyGen provider...")
            provider_job_id = await self.video_provider.create_video(
                text=text,
                avatar_id=avatar_id,
                voice_id=voice_id
            )
            
            self._update_job(job_id, {
                "provider_job_id": provider_job_id,
                "stage": "VIDEO_RENDERING",
                "progress": 10
            })
            
            # 3. Poll for completion (Hackathon fallback for webhooks)
            max_attempts = 60 # 60 * 5s = 5 mins
            for attempt in range(max_attempts):
                await asyncio.sleep(5)
                
                status_data = await self.video_provider.get_video_status(provider_job_id)
                status = status_data["status"]
                progress = status_data.get("progress", 10)
                
                if status == "COMPLETED":
                    self._update_job(job_id, {
                        "status": "READY",
                        "stage": "READY",
                        "progress": 100,
                        "video_url": status_data.get("video_url"),
                        "completed_at": datetime.utcnow()
                    })
                    logger.info(f"Job {job_id} COMPLETED successfully.")
                    return
                elif status == "FAILED":
                    raise Exception(status_data.get("error_message", "Provider failed during rendering"))
                else:
                    self._update_job(job_id, {
                        "progress": progress
                    })
                    
            raise Exception("Video generation timed out after 5 minutes")
            
        except Exception as e:
            logger.error(f"Video job {job_id} failed: {e}")
            self.fallback_to_audio_only(job_id, str(e))
        finally:
            db.close()

    def synthesize_voice(self, text: str, language: str = "Hinglish", voice_id: str = None) -> Dict[str, Any]:
        """
        Creates a new MediaJob in the DB and kicks off the background HeyGen generation task.
        """
        job_id = f"job-{uuid4().hex[:8]}"
        
        v_id = voice_id or self.default_voice_id
        a_id = self.default_avatar_id
        
        db: Session = SessionLocal()
        try:
            new_job = MediaJob(
                id=job_id,
                status="QUEUED",
                stage="SCRIPT",
                progress=0
            )
            db.add(new_job)
            db.commit()
            db.refresh(new_job)
            
            job_record = {
                "id": new_job.id,
                "job_id": new_job.id,
                "status": new_job.status,
                "stage": new_job.stage,
                "progress": new_job.progress
            }
        finally:
            db.close()
            
        # Start background task to hit HeyGen API
        asyncio.create_task(self._process_video_job(job_id, text, a_id, v_id))
        
        return job_record

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        db: Session = SessionLocal()
        try:
            job = db.query(MediaJob).filter(MediaJob.id == job_id).first()
            if not job:
                return None
            return {
                "id": job.id,
                "job_id": job.id,
                "status": job.status,
                "stage": job.stage,
                "progress": job.progress,
                "video_url": job.video_url,
                "audio_url": job.audio_url,
                "visual_url": job.visual_url,
                "error_message": job.error_message
            }
        finally:
            db.close()

    def fallback_to_audio_only(self, job_id: str, error_reason: str = "Video timeout") -> Dict[str, Any]:
        """
        Graceful degradation: fall back to synchronized audio + dynamic visual canvas + captions.
        Updates the DB record accordingly.
        """
        updates = {
            "status": "FALLBACK_AUDIO_ONLY",
            "stage": "READY",
            "progress": 100,
            "error_message": error_reason,
            "audio_url": f"/assets/audio/fallback_{job_id}.mp3",
            "visual_url": f"/assets/visuals/fallback_{job_id}.svg"
        }
        self._update_job(job_id, updates)
        
        return self.get_job_status(job_id)

    def get_health(self) -> Dict[str, str]:
        heygen_ready = "ready" if self.video_provider.is_configured() else "not configured"
        return {
            "video_provider": "heygen",
            "heygen": heygen_ready
        }
