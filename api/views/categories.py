from rest_framework.response import Response
from rest_framework import status
from api.services.categories import TwitchCategoryService  
from api.services.errors import TwitchAPIError
from .base import BaseView
from ..serializers import CategoryResponseSerializer

class TopCategoriesView(BaseView):
    """API view for getting top categories"""
    
    def get(self, request):
        """Get top game categories"""
        try:
            # Get and validate query parameters
            limit = int(request.query_params.get('limit', 10))
            cursor = request.query_params.get('cursor')
            
            # Validate parameters
            self.validate_limit(limit)
            
            # Initialize service and fetch data
            twitch_service = TwitchCategoryService()  # Use TwitchCategoryService
            categories, next_cursor = twitch_service.get_top_categories(
                limit=limit,
                cursor=cursor
            )
            
            # Prepare and serialize response
            response_data = {
                'data': categories,
                'pagination': {'cursor': next_cursor}
            }
            
            serializer = CategoryResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TwitchAPIError as e:
            return self.handle_twitch_api_error(e, 'TopCategoriesView')
        except ValueError as e:
            return self.handle_validation_error('Invalid parameter values')
        except Exception as e:
            return self.handle_unexpected_error(e, 'TopCategoriesView')