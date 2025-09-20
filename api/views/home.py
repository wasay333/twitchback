from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views import View

class HomeView(View):
    """Home view for the API"""
    
    def get(self, request):
        return JsonResponse({
            'message': 'Twitch API Service',
            'version': '1.0',
            'endpoints': {
                'streams': '/api/v1/streams/top/',
                'categories': '/api/v1/categories/top/',
                'sidebar': '/api/v1/streams/sidebar/',
                'search_channels': '/api/v1/search/channels/',
                'search_games': '/api/v1/search/games/',
                'health': '/api/v1/health/'
            }
        })

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Twitch API service is running'
    }, status=status.HTTP_200_OK)
