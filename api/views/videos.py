from rest_framework.response import Response
from rest_framework import status

from api.services.videos import TwitchVideoService   
from api.services.errors import TwitchAPIError
from .base import BaseView
from ..serializers import ChannelVODResponseSerializer

class GetChannelVODsView(BaseView):
    """API view for getting channel VODs"""
    
    def get(self, request, user_login):
        """Get VODs for a specific channel"""
        try:
            # Get and validate query parameters
            limit = int(request.query_params.get('limit', 5))
            cursor = request.query_params.get('cursor')
            
            # Validate parameters
            self.validate_username(user_login)
            self.validate_limit(limit)
            
            # Initialize service and fetch data
            twitch_service = TwitchVideoService()  # Use TwitchVideoService
            vods, next_cursor = twitch_service.get_channel_vods(
                user_login=user_login.strip(),
                limit=limit,
                cursor=cursor
            )
            
            # Prepare and serialize response
            response_data = {
                'data': vods,
                'pagination': {'cursor': next_cursor}
            }
            
            serializer = ChannelVODResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TwitchAPIError as e:
            return self.handle_twitch_api_error(e, 'GetChannelVODsView')
        except ValueError as e:
            return self.handle_validation_error(str(e))
        except Exception as e:
            return self.handle_unexpected_error(e, 'GetChannelVODsView')