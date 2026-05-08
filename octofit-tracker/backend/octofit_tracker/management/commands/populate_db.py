from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from octofit_tracker.models import UserProfile, Team, Activity, Leaderboard, Workout
from django.db import transaction, models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Lösche alte Daten ...'))

            try:
                Activity.objects.all().delete()
                Leaderboard.objects.all().delete()
                Workout.objects.all().delete()
                Team.objects.filter(id__isnull=False).delete()
                UserProfile.objects.filter(id__isnull=False).delete()
                User.objects.all().delete()
            except TypeError:
                self.stdout.write(self.style.WARNING('ORM-Löschung fehlgeschlagen, verwende MongoDB-Fallback.'))
                client = MongoClient('localhost', 27017)
                db = client['octofit_db']
                for collection_name in ['activities', 'leaderboard', 'workouts', 'teams', 'user_profiles']:
                    if collection_name in db.list_collection_names():
                        db[collection_name].drop()
                User.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('Lege Benutzer an ...'))
            # Marvel-Helden
            tony = User.objects.create_user(username='ironman', email='tony@stark.com', password='test123')
            steve = User.objects.create_user(username='captain', email='steve@rogers.com', password='test123')
            natasha = User.objects.create_user(username='blackwidow', email='natasha@shield.com', password='test123')
            # DC-Helden
            clark = User.objects.create_user(username='superman', email='clark@kent.com', password='test123')
            bruce = User.objects.create_user(username='batman', email='bruce@wayne.com', password='test123')
            diana = User.objects.create_user(username='wonderwoman', email='diana@amazon.com', password='test123')

            self.stdout.write(self.style.SUCCESS('Erstelle eindeutigen Email-Index im auth_user Collection...'))
            client = MongoClient('localhost', 27017)
            db = client['octofit_db']
            db['auth_user'].create_index([('email', 1)], unique=True, sparse=True)

            # Profile
            UserProfile.objects.create(user=tony, bio='Genius, Billionaire, Playboy, Philanthropist')
            UserProfile.objects.create(user=steve, bio='Super Soldier')
            UserProfile.objects.create(user=natasha, bio='Spy and Avenger')
            UserProfile.objects.create(user=clark, bio='Man of Steel')
            UserProfile.objects.create(user=bruce, bio='The Dark Knight')
            UserProfile.objects.create(user=diana, bio='Amazon Princess')

            self.stdout.write(self.style.SUCCESS('Lege Teams an ...'))
            marvel = Team.objects.create(name='Team Marvel', description='Marvel Superhelden', owner=tony)
            dc = Team.objects.create(name='Team DC', description='DC Superhelden', owner=clark)
            marvel.members.add(tony, steve, natasha)
            dc.members.add(clark, bruce, diana)

            self.stdout.write(self.style.SUCCESS('Lege Aktivitäten an ...'))
            Activity.objects.create(user=tony, activity_type='running', duration_minutes=30, distance_km=5, calories_burned=400, team=marvel)
            Activity.objects.create(user=steve, activity_type='cycling', duration_minutes=60, distance_km=20, calories_burned=600, team=marvel)
            Activity.objects.create(user=natasha, activity_type='gym', duration_minutes=45, calories_burned=350, team=marvel)
            Activity.objects.create(user=clark, activity_type='running', duration_minutes=40, distance_km=8, calories_burned=500, team=dc)
            Activity.objects.create(user=bruce, activity_type='gym', duration_minutes=90, calories_burned=800, team=dc)
            Activity.objects.create(user=diana, activity_type='yoga', duration_minutes=60, calories_burned=200, team=dc)

            self.stdout.write(self.style.SUCCESS('Lege Leaderboard-Einträge an ...'))
            leaderboard_data = [
                (tony, marvel),
                (steve, marvel),
                (natasha, marvel),
                (clark, dc),
                (bruce, dc),
                (diana, dc),
            ]
            for user_obj, team_obj in leaderboard_data:
                activities = Activity.objects.filter(user=user_obj)
                total_activities = activities.count()
                total_duration = activities.aggregate(models.Sum('duration_minutes'))['duration_minutes__sum'] or 0
                total_calories = activities.aggregate(models.Sum('calories_burned'))['calories_burned__sum'] or 0
                total_distance = activities.aggregate(models.Sum('distance_km'))['distance_km__sum'] or 0.0
                points = (total_activities * 10) + (total_duration // 10) + (total_calories // 50)
                Leaderboard.objects.create(
                    user=user_obj,
                    team=team_obj,
                    total_activities=total_activities,
                    total_duration_minutes=total_duration,
                    total_calories_burned=total_calories,
                    total_distance_km=total_distance,
                    points=points,
                )

            # Nach Punkten sortieren und Ränge vergeben
            for rank, entry in enumerate(Leaderboard.objects.order_by('-points'), start=1):
                entry.rank = rank
                entry.save()

            self.stdout.write(self.style.SUCCESS('Lege Workouts an ...'))
            Workout.objects.create(name='Avengers HIIT', description='Intensives Ganzkörpertraining', difficulty_level='advanced', duration_minutes=45, exercises=[{'name': 'Burpees', 'sets': 5, 'reps': 10}])
            Workout.objects.create(name='Justice League Strength', description='Krafttraining für Helden', difficulty_level='intermediate', duration_minutes=60, exercises=[{'name': 'Deadlifts', 'sets': 4, 'reps': 8}])

            self.stdout.write(self.style.SUCCESS('Fertig!'))
