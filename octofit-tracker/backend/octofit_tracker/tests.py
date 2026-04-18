"""
Tests for OctoFit Tracker API.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile, Team, Activity, Leaderboard, Workout


class UserProfileModelTest(TestCase):
    """Tests for UserProfile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_user_profile(self):
        """Test creating a user profile."""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            profile_picture='http://example.com/pic.jpg'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'Test bio')


class TeamModelTest(TestCase):
    """Tests for Team model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_team(self):
        """Test creating a team."""
        team = Team.objects.create(
            name='Test Team',
            description='Test Description',
            owner=self.user
        )
        self.assertEqual(team.name, 'Test Team')
        self.assertEqual(team.owner, self.user)
    
    def test_add_team_member(self):
        """Test adding a member to team."""
        team = Team.objects.create(
            name='Test Team',
            owner=self.user
        )
        
        member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='pass123'
        )
        
        team.members.add(member)
        self.assertIn(member, team.members.all())


class ActivityModelTest(TestCase):
    """Tests for Activity model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_activity(self):
        """Test creating an activity."""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=300
        )
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'running')
        self.assertEqual(activity.duration_minutes, 30)


class LeaderboardModelTest(TestCase):
    """Tests for Leaderboard model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_leaderboard_entry(self):
        """Test creating a leaderboard entry."""
        entry = Leaderboard.objects.create(
            user=self.user,
            total_activities=5,
            total_duration_minutes=150,
            points=100,
            rank=1
        )
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.rank, 1)
        self.assertEqual(entry.points, 100)


class WorkoutModelTest(TestCase):
    """Tests for Workout model."""
    
    def test_create_workout(self):
        """Test creating a workout."""
        exercises = [
            {'name': 'Pushups', 'sets': 3, 'reps': 10},
            {'name': 'Squats', 'sets': 3, 'reps': 15}
        ]
        
        workout = Workout.objects.create(
            name='Upper Body Workout',
            description='A simple upper body workout',
            difficulty_level='beginner',
            duration_minutes=30,
            exercises=exercises
        )
        self.assertEqual(workout.name, 'Upper Body Workout')
        self.assertEqual(workout.difficulty_level, 'beginner')
        self.assertEqual(len(workout.exercises), 2)


class ActivityAPITest(TestCase):
    """Tests for Activity API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_activity_authenticated(self):
        """Test creating an activity as authenticated user."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'activity_type': 'running',
            'duration_minutes': 30,
            'distance_km': 5.0,
            'calories_burned': 300
        }
        
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_activities(self):
        """Test getting activities."""
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=300
        )
        
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class UserAPITest(TestCase):
    """Tests for User API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_get_users(self):
        """Test getting all users."""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_current_user(self):
        """Test getting current authenticated user."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
