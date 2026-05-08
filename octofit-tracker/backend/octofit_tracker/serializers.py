"""
Serializers for OctoFit Tracker API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Team, Activity, Leaderboard, Workout


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'bio', 'profile_picture', 'created_at', 'updated_at']

    def get_user_id(self, obj):
        """Convert ObjectId to string."""
        return str(obj.user.id)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model."""
    owner_id = serializers.SerializerMethodField()
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'owner_id', 'owner_username', 'members_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_owner_id(self, obj):
        """Convert ObjectId to string."""
        return str(obj.owner.id)

    def get_members_count(self, obj):
        """Get count of team members."""
        return obj.members.count()


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model."""
    user_id = serializers.SerializerMethodField()
    user_username = serializers.CharField(source='user.username', read_only=True)
    team_id = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_username', 'activity_type', 'duration_minutes',
                  'distance_km', 'calories_burned', 'description', 'team_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_user_id(self, obj):
        """Convert ObjectId to string."""
        return str(obj.user.id)

    def get_team_id(self, obj):
        """Convert ObjectId to string."""
        if obj.team:
            return str(obj.team.id)
        return None


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model."""
    user_id = serializers.SerializerMethodField()
    user_username = serializers.CharField(source='user.username', read_only=True)
    team_id = serializers.SerializerMethodField()

    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_username', 'team_id', 'total_activities',
                  'total_duration_minutes', 'total_calories_burned', 'total_distance_km',
                  'rank', 'points', 'updated_at']
        read_only_fields = ['id', 'updated_at']

    def get_user_id(self, obj):
        """Convert ObjectId to string."""
        return str(obj.user.id)

    def get_team_id(self, obj):
        """Convert ObjectId to string."""
        if obj.team:
            return str(obj.team.id)
        return None


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model."""

    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty_level', 'duration_minutes',
                  'exercises', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
