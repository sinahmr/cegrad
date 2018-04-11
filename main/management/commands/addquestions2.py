from django.core.management.base import BaseCommand
from main.models import TheMost2


class Command(BaseCommand):
    help = 'Add questions2'

    def handle(self, *args, **options):
        with open('questions2.txt', encoding="utf8") as file:
            for line in file:
                question = line.rstrip()
                TheMost2.objects.create(text=question)
        print('OK')
