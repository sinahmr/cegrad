from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from main.utils import send_mail
from cegrad.settings import DEBUG


class Command(BaseCommand):
    help = "Change users' password to something random and send email to them"

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='*', type=str, default=None)

    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=False)
        if options['username']:
            users = users.filter(username__in=options['username'])
        for user in users:
            # if user.last_login:
            #     print('Have sent to %s, so will not send now' % user.username)
            #     continue
            try:
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                if DEBUG:
                    email = '%s@example.com' % user.username
                else:
                    email = user.email
                send_mail(email, context={
                    'username': user.username,
                    'password': password
                }, email_template_name='registration')
                print('Sent to %s' % user.username)
            except Exception as e:
                print('Error: %s, %s' % (user.username, e))
        print('OK')
