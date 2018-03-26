import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from main.models import UserProfile


class Command(BaseCommand):
    help = 'Add users'

    def handle(self, *args, **options):
        with open('users.csv') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                username = line[0]
                email = '%s@ce.sharif.edu' % username
                first_name = line[1]
                last_name = line[2]
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, is_staff=True, password='1')
                if len(line) > 3 and line[3] == 'f':
                    UserProfile.objects.create(user=user, profile_picture='default-female.png')
                else:
                    UserProfile.objects.create(user=user, profile_picture='default-male.png')
        print('OK')
