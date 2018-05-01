from django.core.management.base import BaseCommand
from main.models import *
import xlwt


class Command(BaseCommand):
    help = "get users"

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='*', type=str, default=None)

    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=False)

        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet('usernames', cell_overwrite_ok=True)
        sheet.write(0, 0, "id")
        sheet.write(0, 1, "username")
        sheet.write(0, 2, "first name")
        sheet.write(0, 3, "last name")

        for i, user in enumerate(users):
            sheet.write(i+1, 0, user.id)
            sheet.write(i+1, 1, user.username)
            sheet.write(i+1, 2, user.first_name.replace(' ', '\u200c'))
            sheet.write(i+1, 3, user.last_name.replace(' ', '\u200c'))

        book.save('usernames.xls')
        print('OK')
