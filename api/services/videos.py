from typing import Dict, List, Optional, Tuple
import logging
from .base import TwitchAPIBaseService
from .errors import TwitchAPIError
from .channels import TwitchChannelService
from .streamlink import StreamlinkService  

logger = logging.getLogger(__name__)

class TwitchVideoService(TwitchAPIBaseService):
    """Service class for Twitch VOD-related operations"""
    
    def __init__(self):
        super().__init__()
        self.channel_service = TwitchChannelService()
        # Initialize StreamlinkService without OAuth
        self.streamlink_service = StreamlinkService()
    def get_channel_vods(self, user_login: str, limit: int = 5, cursor: Optional[str] = None) -> Tuple[List[Dict], Optional[str]]:
        """Fetch VODs for a channel"""
        limit = min(max(1, limit), 100)
        
        try:
            user_data = self.channel_service.get_user_by_login(user_login)
            user_id = user_data['id']
            
            params = {
                'user_id': user_id,
                'first': limit,
                'type': 'archive'
            }
            if cursor:
                params['after'] = cursor
            
            data = self._make_request('videos', params)
            vods = data.get('data', [])
            cursor = data.get('pagination', {}).get('cursor')
            
            formatted_vods = []
            for vod in vods:
                # Fetch HLS URL using Streamlink
                hls_url = None
                try:
                    hls_url = self.streamlink_service.get_vod_hls_url(vod['id'])
                except TwitchAPIError as e:
                    logger.warning(f"Failed to get HLS URL for VOD {vod['id']}: {e}")
                    # Continue without HLS URL
                
                formatted_vod = {
                    'id': vod['id'],
                    'user_id': vod['user_id'],
                    'user_login': vod['user_login'],
                    'user_name': vod['user_name'],
                    'title': vod['title'],
                    'created_at': vod['created_at'],
                    'duration': vod.get('duration', ''),
                    'view_count': vod.get('view_count', 0),
                    'url': vod['url'],  # Keep for fallback
                    'hls_url': hls_url,  # Add direct HLS URL
                    'thumbnail_url': vod.get('thumbnail_url', ''),
                    'type': vod.get('type', 'archive'),
                    'thumbnail': {
                        'small': vod.get('thumbnail_url', '').replace('%{width}', '320').replace('%{height}', '180'),
                        'medium': vod.get('thumbnail_url', '').replace('%{width}', '640').replace('%{height}', '360'),
                        'large': vod.get('thumbnail_url', '').replace('%{width}', '1920').replace('%{height}', '1080')
                    }
                }
                formatted_vods.append(formatted_vod)
            
            return formatted_vods, cursor
            
        except TwitchAPIError:
            raise
        except Exception as e:
            logger.error(f"Error processing channel VODs: {e}")
            raise TwitchAPIError(f"Error processing channel VODs: {str(e)}", None)