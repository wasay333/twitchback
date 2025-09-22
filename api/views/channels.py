from rest_framework.response import Response
from rest_framework import status
from api.services.channels import TwitchChannelService   
from api.services.streams import TwitchStreamService  
from api.services.errors import TwitchAPIError
from .base import BaseView
from ..serializers import SearchChannelResponseSerializer, ChannelLiveResponseSerializer, StreamResponseSerializer

class SearchChannelsView(BaseView):
    """API view for searching channels"""
    
    def get(self, request):
        """Search for channels"""
        try:
            # Get and validate query parameters
            query = request.query_params.get('query', '').strip()
            limit = int(request.query_params.get('limit', 5))
            cursor = request.query_params.get('cursor')
            
            # Validate required parameters
            self.validate_query(query)
            self.validate_limit(limit)
            
            # Initialize service and fetch data
            twitch_service = TwitchChannelService()  # Use TwitchChannelService
            channels, next_cursor = twitch_service.get_search_channels(
                query=query,
                limit=limit,
                cursor=cursor
            )
            
            # Prepare and serialize response
            response_data = {
                'data': channels,
                'pagination': {'cursor': next_cursor}
            }
            
            serializer = SearchChannelResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TwitchAPIError as e:
            return self.handle_twitch_api_error(e, 'SearchChannelsView')
        except ValueError as e:
            return self.handle_validation_error(str(e))
        except Exception as e:
            return self.handle_unexpected_error(e, 'SearchChannelsView')

class CheckChannelLiveView(BaseView):
    """API view for checking if a channel is live"""
    
    def get(self, request, user_login):
        """Check if a specific channel is live"""
        try:
            # Validate user_login parameter
            self.validate_username(user_login)
            
            # Initialize service and fetch data
            twitch_service = TwitchStreamService()  # Use TwitchStreamService
            streams, next_cursor = twitch_service.get_channel_live_stream(
                user_login=user_login.strip(),
                limit=1
            )
            
            # Prepare and serialize response
            response_data = {
                'data': streams,
                'pagination': {'cursor': next_cursor}
            }
            
            serializer = ChannelLiveResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TwitchAPIError as e:
            return self.handle_twitch_api_error(e, 'CheckChannelLiveView')
        except ValueError as e:
            return self.handle_validation_error(str(e))
        except Exception as e:
            return self.handle_unexpected_error(e, 'CheckChannelLiveView')