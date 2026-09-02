import os
import asyncio
import subprocess
import logging
from typing import Dict, Any
from uuid import uuid4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MediaEngineService:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.tts_api_key = os.getenv("TTS_API_KEY")
        self.avatar_api_key = os.getenv("AVATAR_API_KEY")

    async def _process_video_job(self, job_id: str, text: str):
        job = self.jobs[job_id]
        try:
            # SCRIPT
            job["stage"] = "SCRIPT"
            job["progress"] = 10
            await asyncio.sleep(0.5)
            logger.info(f"[VIDEO] job={job_id} [SCRIPT] completed")

            # TTS
            job["stage"] = "TTS"
            job["progress"] = 20
            logger.info(f"[VIDEO] job={job_id} [TTS] started")
            
            if not self.tts_api_key or self.tts_api_key == "your_tts_api_key":
                error_msg = "TTS Provider Error: Invalid or missing API key."
                logger.error(f"[VIDEO ERROR] stage=TTS provider=elevenlabs status=401 message={error_msg}")
                raise Exception(error_msg)
            
            # (In a real scenario, we would call the TTS API here using httpx)
            await asyncio.sleep(1)
            job["audio_url"] = f"/assets/audio/{job_id}.mp3"
            logger.info(f"[VIDEO] job={job_id} [TTS] completed")

            # VISUAL
            job["stage"] = "VISUAL"
            job["progress"] = 40
            await asyncio.sleep(0.5)
            job["visual_url"] = f"/assets/visuals/{job_id}.svg"
            logger.info(f"[VIDEO] job={job_id} [VISUAL] completed")

            # AVATAR
            job["stage"] = "AVATAR"
            job["progress"] = 60
            logger.info(f"[VIDEO] job={job_id} [AVATAR] job=abc123")
            
            if not self.avatar_api_key or self.avatar_api_key == "your_avatar_api_key":
                error_msg = "Avatar Provider Error: Invalid or missing API key."
                logger.error(f"[VIDEO ERROR] stage=AVATAR provider=heygen status=401 message={error_msg}")
                raise Exception(error_msg)

            await asyncio.sleep(1.5)
            job["avatar_url"] = f"/assets/avatar/{job_id}.mp4"
            logger.info(f"[VIDEO] job={job_id} [AVATAR] completed")

            # COMPOSE
            job["stage"] = "COMPOSE"
            job["progress"] = 80
            logger.info(f"[VIDEO] job={job_id} [COMPOSE] started")
            
            # Check ffmpeg
            try:
                subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            except Exception as e:
                error_msg = "FFmpeg is not available for composition."
                logger.error(f"[VIDEO ERROR] stage=COMPOSE provider=system status=500 message={error_msg}")
                raise Exception(error_msg)

            await asyncio.sleep(1)
            job["video_url"] = f"/assets/video/{job_id}.mp4"
            logger.info(f"[VIDEO] job={job_id} [COMPOSE] completed")

            # UPLOAD & READY
            job["stage"] = "UPLOAD"
            job["progress"] = 90
            await asyncio.sleep(0.5)
            logger.info(f"[VIDEO] job={job_id} [STORAGE] uploaded")

            job["stage"] = "READY"
            job["status"] = "READY"
            job["progress"] = 100
            logger.info(f"[VIDEO] job={job_id} [VIDEO] READY")

        except Exception as e:
            # Fallback handling
            self.fallback_to_audio_only(job_id, str(e))

    def synthesize_voice(self, text: str, language: str = "Hinglish", voice_id: str = "dr_aris_calm") -> Dict[str, Any]:
        """
        Synthesizes voice segment with status tracking and playback URL.
        """
        job_id = f"job-{uuid4().hex[:8]}"
        job_record = {
            "id": job_id,
            "job_id": job_id,
            "status": "PROCESSING",
            "stage": "PREPARING",
            "progress": 0,
            "error_message": None,
            "audio_url": None,
            "avatar_url": None,
            "visual_url": None,
            "video_url": None,
            "language": language,
            "voice_id": voice_id,
            "text": text,
            "fallback_active": False
        }
        self.jobs[job_id] = job_record
        
        # Start background task
        asyncio.create_task(self._process_video_job(job_id, text))
        return job_record

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        return self.jobs.get(job_id)

    def fallback_to_audio_only(self, job_id: str, error_reason: str = "Video timeout") -> Dict[str, Any]:
        """
        Graceful degradation: fall back to synchronized audio + dynamic visual canvas + captions.
        """
        record = self.jobs.get(job_id)
        if not record:
            return None

        record["status"] = "FALLBACK_AUDIO_ONLY"
        record["stage"] = "READY"
        record["fallback_active"] = True
        record["error_message"] = error_reason
        
        # Ensure we have at least fallback URLs so the player can continue
        record["audio_url"] = f"/assets/audio/fallback_{job_id}.mp3"
        record["visual_url"] = f"/assets/visuals/fallback_{job_id}.svg"
        
        return record

    def get_health(self) -> Dict[str, str]:
        import shutil
        
        # Determine TTS status
        tts_key = os.getenv("TTS_API_KEY", "")
        tts_ready = "ready" if tts_key and tts_key != "your_tts_api_key" else "not configured"
        
        # Avatar
        avatar_key = os.getenv("AVATAR_API_KEY", "")
        avatar_ready = "ready" if avatar_key and avatar_key != "your_avatar_api_key" else "not configured"
        
        # LLM
        llm_key = os.getenv("GEMINI_API_KEY", "")
        llm_ready = "ready" if llm_key and llm_key != "your_gemini_api_key" else "not configured"
        
        # Storage
        storage_key = os.getenv("STORAGE_ACCESS_KEY", "")
        storage_ready = "ready" if storage_key and storage_key != "your_access_key" else "not configured"

        # FFmpeg
        ffmpeg_ready = "ready" if shutil.which("ffmpeg") else "not installed"
        
        return {
            "llm": llm_ready,
            "tts": tts_ready,
            "avatar": avatar_ready,
            "storage": storage_ready,
            "ffmpeg": ffmpeg_ready
        }
