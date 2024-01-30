# yourapp/management/commands/generate_dummy_data.py
from django.core.management.base import BaseCommand
from model_bakery import baker
from cinema.models import *

class Command(BaseCommand):
    help = 'Generate and save dummy data for all models'

    def handle(self, *args, **options):
        
        # genre = baker.make(Genre, _quantity=10)
        # movie = baker.make(Movie, genre=baker.random_element(genre), _quantity=20)
        # tvshow = baker.make(TVShow, genre=baker.random_element(genre), _quantity=10)
        # season = baker.make(Season, tvshow=baker.random_element(tvshow), _quantity=50)
        # episode = baker.make(Episode, season=baker.random_element(season), _quantity=100)
        # cast = baker.make(Cast, _quantity=100)
        # ...
        
        models_to_generate = [Genre, Movie, TVShow, Season, Episode, Cast, Role, Reviewer, Comment]

        for model in models_to_generate:
            baker.make(model, _quantity=20, _create_files=True)
            
        self.stdout.write(self.style.SUCCESS('Dummy data generated and saved successfully.'))
