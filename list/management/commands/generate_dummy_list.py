# yourapp/management/commands/generate_dummy_data.py
from django.core.management.base import BaseCommand
from model_bakery import baker
from list.models import *

class Command(BaseCommand):
    help = 'Generate and save dummy data for all models'

    def handle(self, *args, **options):
            
        models_to_generate = [List, ListItems]

        for model in models_to_generate:
            baker.make(model, _quantity=20, _create_files=True)
            
        self.stdout.write(self.style.SUCCESS('Dummy data generated and saved successfully.'))
