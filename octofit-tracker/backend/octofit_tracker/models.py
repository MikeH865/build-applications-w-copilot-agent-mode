"""
MongoDB models for OctoFit Tracker app.
"""
from django.db import models
from django.contrib.auth.models import User

from bson import ObjectId


class UserProfile(models.Model):
    """Extended user profile for OctoFit Tracker."""

    id = djongo_models.ObjectIdField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f'{self.user.username} Profile'


class Team(models.Model):
    """Team model for group management."""
    id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity logging model."""
    id = djongo_models.ObjectIdField(primary_key=True)
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('gym', 'Gym'),
        ('yoga', 'Yoga'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration_minutes = models.IntegerField()  # Duration in minutes
    distance_km = models.FloatField(blank=True, null=True)
    calories_burned = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.activity_type}'


class Leaderboard(models.Model):
    """Leaderboard entry model for rankings."""
    id = djongo_models.ObjectIdField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard_entry')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='leaderboard')
    total_activities = models.IntegerField(default=0)
    total_duration_minutes = models.IntegerField(default=0)
    total_calories_burned = models.IntegerField(default=0)
    total_distance_km = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-points', 'rank']

    def __str__(self):
        return f'{self.user.username} - Rank {self.rank}'


class Workout(models.Model):
    """Personalized workout suggestion model."""
    id = djongo_models.ObjectIdField(primary_key=True)
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration_minutes = models.IntegerField()
    exercises = models.JSONField(default=list)  # List of exercise objects
    target_audience = models.ManyToManyField(User, related_name='suggested_workouts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
