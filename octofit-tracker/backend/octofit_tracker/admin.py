"""
Django admin configuration for OctoFit Tracker.
"""
from django.contrib import admin
from .models import UserProfile, Team, Activity, Leaderboard, Workout


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin for Team model."""
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('members',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin for Activity model."""
    list_display = ('user', 'activity_type', 'duration_minutes', 'created_at')
    search_fields = ('user__username', 'activity_type')
    list_filter = ('activity_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin for Leaderboard model."""
    list_display = ('user', 'rank', 'points', 'total_activities', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('rank', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin for Workout model."""
    list_display = ('name', 'difficulty_level', 'duration_minutes', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('difficulty_level', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('target_audience',)