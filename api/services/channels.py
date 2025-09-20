from typing import Dict, List, Optional, Tuple
import logging
from .base import TwitchAPIBaseService
from .errors import TwitchAPIError

logger = logging.getLogger(__name__)

class TwitchChannelService(TwitchAPIBaseService):
    """Service class for Twitch channel-related operations"""
    
    def get_search_channels(self, query: str, limit: int = 5, cursor: Optional[str] = None) -> Tuple[List[Dict], Optional[str]]:
        """Search for channels matching the query"""
        limit = min(max(1, limit), 100)
        
        params = {
            'query': query,
            'first': limit
        }
        if cursor:
            params['after'] = cursor
        
        try:
            data = self._make_request('search/channels', params)
            channels = data.get('data', [])
            cursor = data.get('pagination', {}).get('cursor')
            
            formatted_channels = []
            for channel in channels:
                formatted_channel = {
                    'id': channel['id'],
                    'broadcaster_login': channel['broadcaster_login'],
                    'display_name': channel['display_name'],
                    'description': channel.get('description', ''),
                    'thumbnail_url': channel['thumbnail_url'],
                    'is_live': False
                }
                formatted_channels.append(formatted_channel)
            
            return formatted_channels, cursor
            
        except TwitchAPIError:
            raise
        except Exception as e:
            logger.error(f"Error processing search channels: {e}")
            raise TwitchAPIError(f"Error processing search channels: {str(e)}", None)
    
    def get_user_by_login(self, user_login: str) -> Dict:
        """Get user information by login name to retrieve user_id"""
        params = {
            'login': user_login
        }
        
        try:
            data = self._make_request('users', params)
            users = data.get('data', [])
            
            if not users:
                raise TwitchAPIError(f"User '{user_login}' not found", 404)
            
            return users[0]
            
        except TwitchAPIError:
            raise
        except Exception as e:
            logger.error(f"Error fetching user by login: {e}")
            raise TwitchAPIError(f"Error fetching user: {str(e)}", None)
