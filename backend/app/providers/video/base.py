from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class VideoProvider(ABC):
    """
    Abstract interface for AI Video Generation Providers.
    """
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if provider has valid configuration."""
        pass

    @abstractmethod
    async def create_video(self, text: str, avatar_id: str, voice_id: str) -> str:
        """
        Initiates a video generation job.
        Returns the provider's specific job_id.
        """
        pass

    @abstractmethod
    async def get_video_status(self, provider_job_id: str) -> Dict[str, Any]:
        """
        Checks the status of a video generation job.
        Returns a dictionary containing:
        - status: str (e.g., 'PROCESSING', 'COMPLETED', 'FAILED')
        - progress: int (0-100)
        - video_url: str (if completed)
        - error_message: str (if failed)
        """
        pass
        
    @abstractmethod
    async def cancel_video(self, provider_job_id: str) -> bool:
        """Cancels an in-progress video generation."""
        pass
