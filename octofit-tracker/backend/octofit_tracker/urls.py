"""
URL configuration for OctoFit Tracker API.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
import os

from .views import (
    UserViewSet, UserProfileViewSet, TeamViewSet,
    ActivityViewSet, LeaderboardViewSet, WorkoutViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')


class APIRootView(APIView):
    """API Root view."""
    def get(self, request):
        """Return API root information."""
        return Response({
            'message': 'OctoFit Tracker API',
            'version': '1.0.0',
            'endpoints': {
                'users': request.build_absolute_uri('/api/users/'),
                'profiles': request.build_absolute_uri('/api/profiles/'),
                'teams': request.build_absolute_uri('/api/teams/'),
                'activities': request.build_absolute_uri('/api/activities/'),
                'leaderboard': request.build_absolute_uri('/api/leaderboard/'),
                'workouts': request.build_absolute_uri('/api/workouts/'),
            }
        })


api_root = APIRootView.as_view()

# Determine base URL based on environment
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),  # Root endpoint
    path('api/', api_root, name='api-root'),  # API root endpoint
    path('api/', include(router.urls)),  # Include router URLs
]