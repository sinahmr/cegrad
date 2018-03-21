from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import UserProfile


class Command(BaseCommand):
    help = 'Add users'

    def handle(self, *args, **options):
        with open('users.txt') as file:
            for line in file:
                username = line.rstrip()
                email = '%s@ce.sharif.edu' % username
                user = User.objects.create_user(username=username, email=email, is_staff=True, password='1')
                UserProfile.objects.create(user=user)
        print('OK')
