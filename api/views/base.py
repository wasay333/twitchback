from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

from api.services.errors import TwitchAPIError


logger = logging.getLogger(__name__)

class BaseView(APIView):
    """Base view with common error handling and validation for Twitch API views"""
    
    def handle_twitch_api_error(self, e: TwitchAPIError, view_name: str):
        """Centralized error handling for TwitchAPIError"""
        logger.error(f"Twitch API error in {view_name}: {e}")
        
        error_status = status.HTTP_400_BAD_REQUEST
        if e.status_code == 401:
            error_status = status.HTTP_401_UNAUTHORIZED
        elif e.status_code == 403:
            error_status = status.HTTP_403_FORBIDDEN
        elif e.status_code == 429:
            error_status = status.HTTP_429_TOO_MANY_REQUESTS
        elif e.status_code == 500:
            error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        return Response(
            {'error': str(e), 'status_code': e.status_code},
            status=error_status
        )
    
    def handle_validation_error(self, message: str):
        """Handle validation errors"""
        return Response(
            {'error': message},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def handle_unexpected_error(self, e: Exception, view_name: str):
        """Handle unexpected errors"""
        logger.error(f"Unexpected error in {view_name}: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    def validate_limit(self, limit: int, max_limit: int = 15, min_limit: int = 1):
        """Validate limit parameter"""
        if limit < min_limit or limit > max_limit:
            raise ValueError(f'Limit must be between {min_limit} and {max_limit}')
        return True
    
    def validate_username(self, username: str):
        """Validate username parameter"""
        if not username or not username.strip():
            raise ValueError('Invalid username')
        return True
    
    def validate_query(self, query: str):
        """Validate query parameter"""
        if not query or not query.strip():
            raise ValueError('Query parameter is required')
        return True
