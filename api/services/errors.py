import logging
from typing import Optional

logger = logging.getLogger(__name__)

class TwitchAPIError(Exception):
    """Custom exception for Twitch API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)
