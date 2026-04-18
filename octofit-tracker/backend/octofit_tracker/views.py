"""
Views for OctoFit Tracker API.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.db.models import Sum, Count

from .models import UserProfile, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, UserProfileSerializer, TeamSerializer,
    ActivitySerializer, LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current authenticated user."""
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model."""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a team."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team."""
        team = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({'status': 'member added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from the team."""
        team = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({'status': 'member removed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model."""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Set the user to the current user when creating an activity."""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Filter activities by user if not admin."""
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id')
        team_id = self.request.query_params.get('team_id')
        activity_type = self.request.query_params.get('activity_type')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)

        return queryset.order_by('-created_at')

    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities."""
        if request.user.is_authenticated:
            activities = Activity.objects.filter(user=request.user).order_by('-created_at')
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Leaderboard model."""
    queryset = Leaderboard.objects.all().order_by('-points', 'rank')
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter leaderboard by team if provided."""
        queryset = Leaderboard.objects.all().order_by('-points', 'rank')
        team_id = self.request.query_params.get('team_id')

        if team_id:
            queryset = queryset.filter(team_id=team_id)

        return queryset

    @action(detail=False, methods=['post'])
    def update_leaderboard(self, request):
        """Update leaderboard based on user activities."""
        try:
            users = User.objects.all()

            for user in users:
                activities = Activity.objects.filter(user=user)

                total_activities = activities.count()
                total_duration = activities.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
                total_calories = activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
                total_distance = activities.aggregate(Sum('distance_km'))['distance_km__sum'] or 0.0

                # Calculate points (simple formula)
                points = (total_activities * 10) + (total_duration // 10) + (total_calories // 50)

                leaderboard_entry, created = Leaderboard.objects.get_or_create(user=user)
                leaderboard_entry.total_activities = total_activities
                leaderboard_entry.total_duration_minutes = total_duration
                leaderboard_entry.total_calories_burned = total_calories
                leaderboard_entry.total_distance_km = total_distance
                leaderboard_entry.points = points
                leaderboard_entry.save()

            # Update ranks
            leaderboard_entries = Leaderboard.objects.order_by('-points')
            for rank, entry in enumerate(leaderboard_entries, 1):
                entry.rank = rank
                entry.save()

            return Response({'status': 'leaderboard updated'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WorkoutViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Workout model."""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter workouts by difficulty level or get personalized suggestions."""
        queryset = Workout.objects.all()
        difficulty = self.request.query_params.get('difficulty')

        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        return queryset

    @action(detail=False, methods=['get'])
    def suggested_workouts(self, request):
        """Get personalized workout suggestions for current user."""
        if request.user.is_authenticated:
            # Simple suggestion logic based on user's recent activities
            user_activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:5]

            if not user_activities.exists():
                # Suggest beginner workouts if no activities
                workouts = Workout.objects.filter(difficulty_level='beginner')
            else:
                # Suggest workouts based on activity frequency
                activity_count = Activity.objects.filter(user=request.user).count()
                if activity_count < 5:
                    difficulty = 'beginner'
                elif activity_count < 15:
                    difficulty = 'intermediate'
                else:
                    difficulty = 'advanced'

                workouts = Workout.objects.filter(difficulty_level=difficulty)

            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)