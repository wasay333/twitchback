from django.http import JsonResponse
def root_view(request):
    return JsonResponse({"message": "Welcome to the twitch Backend","api-endpoint": "/api/v1/"})
