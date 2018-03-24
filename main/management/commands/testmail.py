from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage


class Command(BaseCommand):
    help = 'Test mail'

    def handle(self, *args, **options):
        email = EmailMessage('Hello', 'World', to=['mohammadsadegh.ce@gmail.com'])
        email.send()
        print('OK')
