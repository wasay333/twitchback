from django.urls import path
from .views import (
    HomeView,
    health_check,
    TopLiveStreamsView,
    TopCategoriesView,
    SidebarStreamsView,
    SearchChannelsView,
    CheckChannelLiveView,
    GetChannelVODsView,
    SearchGamesView,
    GetGameStreamsView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('health/', health_check, name='health-check'),
    path('streams/top/', TopLiveStreamsView.as_view(), name='top-live-streams'),
    path('categories/top/', TopCategoriesView.as_view(), name='top-categories'),
    path('streams/sidebar/', SidebarStreamsView.as_view(), name='sidebar-streams'),
    # Channel Search Endpoints
    path('search/channels/', SearchChannelsView.as_view(), name='search-channels'),
    path('channels/<str:user_login>/live/', CheckChannelLiveView.as_view(), name='check-channel-live'),
    path('channels/<str:user_login>/vods/', GetChannelVODsView.as_view(), name='get-channel-vods'),
    # Game Search Endpoints
    path('search/games/', SearchGamesView.as_view(), name='search-games'),
    path('games/<str:game_id>/streams/', GetGameStreamsView.as_view(), name='get-game-streams')
]