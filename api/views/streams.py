from rest_framework.response import Response
from rest_framework import status

from api.services.streams import TwitchStreamService  # Import TwitchStreamService
from api.services.errors import TwitchAPIError

from .base import BaseView
from ..serializers import StreamResponseSerializer, SidebarResponseSerializer

class TopLiveStreamsView(BaseView):
    """API view for getting top live streams"""
    
    def get(self, request):
        """Get top live streams"""
        try:
            # Get and validate query parameters
            limit = int(request.query_params.get('limit', 10))
            language = request.query_params.get('language')
            game_id = request.query_params.get('game_id')
            cursor = request.query_params.get('cursor')
            
            # Validate parameters
            self.validate_limit(limit)
            
            # Initialize service and fetch data
            twitch_service = TwitchStreamService()  # Use TwitchStreamService
            streams, next_cursor = twitch_service.get_top_live_streams(
                limit=limit,
                language=language,
                game_id=game_id,
                cursor=cursor,
                sidebar=False
            )
            
            # Prepare and serialize response
            response_data = {
                'data': streams,
                'pagination': {'cursor': next_cursor}
            }
            
            serializer = StreamResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TwitchAPIError as e:
            return self.handle_twitch_api_error(e, 'TopLiveStreamsView')
        except ValueError as e:
            return self.handle_validation_error('Invalid parameter values')
        except Exception as e:
            return self.handle_unexpected_error(e, 'TopLiveStreamsView')

class SidebarStreamsView(BaseView):
    """API view for getting minimal stream data for sidebar"""
    
    def get(self, request):
        """Get sidebar streams with minimal data"""
        try:
            # Get and validate query parameters
            limit = int(request.query_params.get('limit', 5))
            language = request.query_params.get('language')
            game_id = request.query_params.get('game_id')
            
            # Validate parameters (smaller limit for sidebar)
            self.validate_limit(limit, max_limit=20)
            
            # Initialize service and fetch data
            twitch_service = TwitchStreamService()  # Use TwitchStreamService
            streams, next_cursor = twitch_service.get_top_live_streams(
                limit=limit,
                language=language,
                game_id=game_id,
                cursor=None,  # No pagination for sidebar
                sidebar=True
            )
            
            # Prepare and serialize response
            response_data = {
                'data': streams,
                'pagination': {'cursor': next_cursor}
            }
            
            serializer = SidebarResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TwitchAPIError as e:
            return self.handle_twitch_api_error(e, 'SidebarStreamsView')
        except ValueError as e:
            return self.handle_validation_error('Invalid parameter values')
        except Exception as e:
            return self.handle_unexpected_error(e, 'SidebarStreamsView')