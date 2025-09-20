import logging
from typing import Optional
from streamlink import Streamlink
from streamlink.stream import HLSStream
from .errors import TwitchAPIError

logger = logging.getLogger(__name__)

class StreamlinkService:
    """Service class for extracting direct HLS URLs using Streamlink for public APIs"""
    
    def __init__(self):
        self.session = Streamlink()
        # Set timeout for reliability
        self.session.set_option("http-timeout", 10)
    
    def get_stream_hls_url(self, user_login: str, quality: str = "best") -> Optional[str]:
        """Extract direct HLS URL for a live stream"""
        url = f"https://twitch.tv/{user_login}"
        try:
            streams = self.session.streams(url)
            if not streams:
                logger.warning(f"No streams available for {user_login}")
                raise TwitchAPIError(f"No streams available for {user_login}", 404)
            
            hls_streams = {name: stream for name, stream in streams.items() if isinstance(stream, HLSStream)}
            if not hls_streams:
                logger.warning(f"No HLS streams available for {user_login}")
                raise TwitchAPIError(f"No HLS streams available for {user_login}", 404)
            
            if quality not in hls_streams:
                available = list(hls_streams.keys())
                logger.warning(f"Quality '{quality}' not available for {user_login}. Options: {available}")
                raise TwitchAPIError(f"Quality '{quality}' not available. Options: {available}", 400)
            
            direct_m3u8_url = hls_streams[quality].url
            logger.info(f"Extracted HLS URL for {user_login}: {direct_m3u8_url}")
            return direct_m3u8_url
        
        except Exception as e:
            logger.error(f"Error extracting HLS URL for {user_login}: {e}")
            raise TwitchAPIError(f"Failed to extract HLS URL: {str(e)}", None)
    
    def get_vod_hls_url(self, vod_id: str, quality: str = "best") -> Optional[str]:
        """Extract direct HLS URL for a VOD"""
        url = f"https://www.twitch.tv/videos/{vod_id}"
        try:
            streams = self.session.streams(url)
            if not streams:
                logger.warning(f"No VOD streams available for ID {vod_id}")
                raise TwitchAPIError(f"No VOD streams available for ID {vod_id}", 404)
            
            hls_streams = {name: stream for name, stream in streams.items() if isinstance(stream, HLSStream)}
            if not hls_streams:
                logger.warning(f"No HLS streams available for VOD {vod_id}")
                raise TwitchAPIError(f"No HLS streams available for VOD {vod_id}", 404)
            
            if quality not in hls_streams:
                available = list(hls_streams.keys())
                logger.warning(f"Quality '{quality}' not available for VOD {vod_id}. Options: {available}")
                raise TwitchAPIError(f"Quality '{quality}' not available. Options: {available}", 400)
            
            direct_m3u8_url = hls_streams[quality].url
            logger.info(f"Extracted HLS URL for VOD {vod_id}: {direct_m3u8_url}")
            return direct_m3u8_url
        
        except Exception as e:
            logger.error(f"Error extracting HLS URL for VOD {vod_id}: {e}")
            raise TwitchAPIError(f"Failed to extract VOD HLS URL: {str(e)}", None)