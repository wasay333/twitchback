from rest_framework.response import Response
from rest_framework import status
from api.services.categories import TwitchCategoryService 
from api.services.streams import TwitchStreamService   
from api.services.errors import TwitchAPIError
from .base import BaseView
from ..serializers import SearchGameResponseSerializer, StreamResponseSerializer

class SearchGamesView(BaseView):
    """API view for searching games"""
    
    def get(self, request):
        """Search for games/categories"""
        try:
            # Get and validate query parameters
            query = request.query_params.get('query', '').strip()
            limit = int(request.query_params.get('limit', 5))
            cursor = request.query_params.get('cursor')
            
            # Validate required parameters
            self.validate_query(query)
            self.validate_limit(limit)
            
            # Initialize service and fetch data
            twitch_service = TwitchCategoryService()  # Use TwitchCategoryService
            games, next_cursor = twitch_service.get_search_games(
                query=query,
                limit=limit,
                cursor=cursor
            )
            
            # Prepare and serialize response
            response_data = {
                'data': games,
                'pagination': {'cursor': next_cursor}
            }
            
            serializer = SearchGameResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TwitchAPIError as e:
            return self.handle_twitch_api_error(e, 'SearchGamesView')
        except ValueError as e:
            return self.handle_validation_error(str(e))
        except Exception as e:
            return self.handle_unexpected_error(e, 'SearchGamesView')

class GetGameStreamsView(BaseView):
    """API view for getting streams for a specific game"""
    
    def get(self, request, game_id):
        """Get live streams for a specific game"""
        try:
            # Get and validate query parameters
            limit = int(request.query_params.get('limit', 5))
            cursor = request.query_params.get('cursor')
            
            # Validate parameters
            if not game_id or not game_id.strip():
                raise ValueError('Invalid game ID')
            self.validate_limit(limit)
            
            # Initialize service and fetch data
            twitch_service = TwitchStreamService()  # Use TwitchStreamService
            streams, next_cursor = twitch_service.get_game_streams(
                game_id=game_id.strip(),
                limit=limit,
                cursor=cursor
            )
            
            # Prepare and serialize response
            response_data = {
                'data': streams,
                'pagination': {'cursor': next_cursor}
            }
            
            serializer = StreamResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TwitchAPIError as e:
            return self.handle_twitch_api_error(e, 'GetGameStreamsView')
        except ValueError as e:
            return self.handle_validation_error(str(e))
        except Exception as e:
            return self.handle_unexpected_error(e, 'GetGameStreamsView')