import requests
import logging
from typing import Dict, Optional
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .errors import TwitchAPIError

logger = logging.getLogger(__name__)

class TwitchAPIBaseService:
    """Base service class for Twitch API configuration and request handling"""
    
    BASE_URL = 'https://api.twitch.tv/helix'
    
    def __init__(self):
        # Validate required settings
        if not all([settings.TWITCH_CLIENT_ID, settings.TWITCH_ACCESS_TOKEN]):
            raise ImproperlyConfigured(
                "TWITCH_CLIENT_ID and TWITCH_ACCESS_TOKEN must be set in environment variables"
            )
        
        self.client_id = settings.TWITCH_CLIENT_ID
        self.access_token = settings.TWITCH_ACCESS_TOKEN
        self.headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None, method: str = 'GET') -> Dict:
        """Make authenticated request to Twitch API with comprehensive error handling"""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        try:
            logger.info(f"Making Twitch API request: {method} {url}")
            response = (
                requests.post(url, headers=self.headers, json=params or {}, timeout=30)
                if method.upper() == 'POST'
                else requests.get(url, headers=self.headers, params=params or {}, timeout=30)
            )
            
            # Attempt to parse JSON for error details
            try:
                error_data = response.json()
            except (ValueError, KeyError):
                error_data = {'error': 'Unknown', 'message': response.text}
            
            # Handle Twitch-specific HTTP status codes
            if response.status_code == 200:
                logger.info(f"Twitch API request successful: {len(error_data.get('data', []))} items returned")
                return error_data
            elif response.status_code == 400:
                error_msg = error_data.get('message', 'Bad Request')
                logger.error(f"Twitch API 400 Bad Request: {error_msg}")
                raise TwitchAPIError(f"Bad Request: {error_msg}", 400)
            elif response.status_code == 401:
                error_msg = error_data.get('message', 'Unauthorized')
                logger.error(f"Twitch API 401 Unauthorized: {error_msg}")
                raise TwitchAPIError(f"Unauthorized: {error_msg}. Check access token.", 401)
            elif response.status_code == 403:
                error_msg = error_data.get('message', 'Forbidden')
                logger.error(f"Twitch API 403 Forbidden: {error_msg}")
                raise TwitchAPIError(f"Forbidden: {error_msg}", 403)
            elif response.status_code == 404:
                error_msg = error_data.get('message', 'Not Found')
                logger.error(f"Twitch API 404 Not Found: {error_msg}")
                raise TwitchAPIError(f"Not Found: {error_msg}", 404)
            elif response.status_code == 429:
                error_msg = error_data.get('message', 'Rate limit exceeded')
                retry_after = error_data.get('retry_after', 0)
                logger.warning(f"Twitch API 429 Rate limit exceeded: {error_msg}. Retry after: {retry_after}s")
                raise TwitchAPIError(f"Rate limit exceeded: {error_msg}. Retry after {retry_after}s", 429)
            elif response.status_code == 500:
                error_msg = error_data.get('message', 'Internal Server Error')
                logger.error(f"Twitch API 500 Internal Server Error: {error_msg}")
                raise TwitchAPIError(f"Internal Server Error: {error_msg}", 500)
            else:
                error_msg = error_data.get('message', f'HTTP {response.status_code}')
                logger.error(f"Twitch API error {response.status_code}: {error_msg}")
                raise TwitchAPIError(f"API request failed: {error_msg}", response.status_code)
            
        except requests.exceptions.Timeout:
            logger.error("Twitch API request timeout")
            raise TwitchAPIError("Request timeout after 30 seconds", None)
        except requests.exceptions.ConnectionError:
            logger.error("Twitch API connection error")
            raise TwitchAPIError("Failed to connect to Twitch API", None)
        except requests.exceptions.RequestException as e:
            logger.error(f"Twitch API request error: {e}")
            raise TwitchAPIError(f"Request failed: {str(e)}", None)
        except Exception as e:
            logger.error(f"Unexpected error in Twitch API request: {e}")
            raise TwitchAPIError(f"Unexpected error: {str(e)}", None)
