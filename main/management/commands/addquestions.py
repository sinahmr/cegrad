from django.core.management.base import BaseCommand
from main.models import TheMost


class Command(BaseCommand):
    help = 'Add questions'

    def handle(self, *args, **options):
        with open('questions.txt', encoding="utf8") as file:
            for line in file:
                question = line.rstrip()
                TheMost.objects.create(text=question)
        print('OK')
