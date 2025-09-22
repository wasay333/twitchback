from typing import Dict, List, Optional, Tuple
import logging

from api.services.channels import TwitchChannelService
from .base import TwitchAPIBaseService
from .errors import TwitchAPIError
from .streamlink import StreamlinkService 

logger = logging.getLogger(__name__)

class TwitchStreamService(TwitchAPIBaseService):
    """Service class for Twitch stream-related operations"""
    
    def __init__(self):
        super().__init__()
        # Initialize StreamlinkService (pass OAuth token if available)
        self.channel_service = TwitchChannelService()
        self.streamlink_service = StreamlinkService()    
    def get_top_live_streams(self, 
                            limit: int = 10, 
                            language: Optional[str] = None,
                            game_id: Optional[str] = None,
                            cursor: Optional[str] = None,
                            sidebar: bool = False) -> Tuple[List[Dict], Optional[str]]:
        """Get top live streams with cursor support"""
        limit = min(max(1, limit), 100)
        
        params = {
            'first': limit,
            'type': 'live'
        }
        if not sidebar and cursor:
            params['after'] = cursor
        if language:
            params['language'] = language
        if game_id:
            params['game_id'] = game_id
        
        try:
            data = self._make_request('streams', params)
            streams = data.get('data', [])
            cursor = data.get('pagination', {}).get('cursor')
            
            formatted_streams = []
            for stream in streams:
                stream['_sidebar_only'] = sidebar
                formatted_stream = self._format_stream_data(stream)
                formatted_streams.append(formatted_stream)
            
            return formatted_streams, cursor
            
        except TwitchAPIError:
            raise
        except Exception as e:
            logger.error(f"Error processing streams data: {e}")
            raise TwitchAPIError(f"Error processing streams: {str(e)}", None)
    
    def get_channel_live_stream(self, user_login: str, limit: int = 1) -> Tuple[List[Dict], Optional[str]]:
        """Check if a channel is live and get stream details"""
        limit = min(max(1, limit), 100)
        
        params = {
            'user_login': user_login,
            'type': 'live',
            'first': limit
        }
        
        try:
            data = self._make_request('streams', params)
            streams = data.get('data', [])
            cursor = data.get('pagination', {}).get('cursor')
            
            formatted_streams = []
            for stream in streams:
                formatted_stream = self._format_stream_data(stream)
                formatted_stream['is_live'] = True
                formatted_streams.append(formatted_stream)
            
            return formatted_streams, cursor
            
        except TwitchAPIError:
            raise
        except Exception as e:
            logger.error(f"Error processing channel live stream: {e}")
            raise TwitchAPIError(f"Error processing channel live stream: {str(e)}", None)
    
    def get_game_streams(self, game_id: str, limit: int = 5, cursor: Optional[str] = None) -> Tuple[List[Dict], Optional[str]]:
        """Fetch live streams for a game"""
        limit = min(max(1, limit), 100)
        
        params = {
            'game_id': game_id,
            'first': limit,
            'type': 'live'
        }
        if cursor:
            params['after'] = cursor
        
        try:
            data = self._make_request('streams', params)
            streams = data.get('data', [])
            cursor = data.get('pagination', {}).get('cursor')
            
            formatted_streams = []
            for stream in streams:
                formatted_stream = self._format_stream_data(stream)
                formatted_streams.append(formatted_stream)
            
            return formatted_streams, cursor
            
        except TwitchAPIError:
            raise
        except Exception as e:
            logger.error(f"Error processing game streams: {e}")
            raise TwitchAPIError(f"Error processing game streams: {str(e)}", None)
    
    def _format_stream_data(self, stream: Dict) -> Dict:
        """Format raw stream data from Twitch API for consistent output"""
        try:
            # Fetch HLS URL using Streamlink
            hls_url = None
            try:
                hls_url = self.streamlink_service.get_stream_hls_url(stream['user_login'])
            except TwitchAPIError as e:
                logger.warning(f"Failed to get HLS URL for {stream['user_login']}: {e}")
                # Continue without HLS URL to avoid breaking the response
            
            formatted_stream = {
                'user_name': stream['user_name'],
                'viewer_count': stream['viewer_count'],
                'thumbnail_url': stream['thumbnail_url'],
                'stream_url': f"https://twitch.tv/{stream['user_login']}",  # Keep for fallback
                'hls_url': hls_url,  # Add direct HLS URL
                'thumbnail': {
                    'small': stream['thumbnail_url'].replace('{width}', '320').replace('{height}', '180'),
                    'medium': stream['thumbnail_url'].replace('{width}', '640').replace('{height}', '360'),
                    'large': stream['thumbnail_url'].replace('{width}', '1920').replace('{height}', '1080')
                }
            }
            if not stream.get('_sidebar_only', False):
                formatted_stream.update({
                    'id': stream['id'],
                    'user_id': stream['user_id'],
                    'user_login': stream['user_login'],
                    'game_id': stream.get('game_id'),
                    'game_name': stream.get('game_name', 'No Category'),
                    'title': stream['title'],
                    'started_at': stream['started_at'],
                    'language': stream['language'],
                    'tags': stream.get('tags', []),
                    'is_mature': stream.get('is_mature', False),
                    'type': stream.get('type', 'live'),
                    'profile_image_url': None
                })
            return formatted_stream
        except KeyError as e:
            logger.error(f"Missing required field in stream data: {e}")
            raise TwitchAPIError(f"Invalid stream data format: missing {e}", None)