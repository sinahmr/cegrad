from django.core.management.base import BaseCommand
from main.models import *
import xlwt
import os


class Command(BaseCommand):
    help = "get opinions"

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='*', type=str, default=None)

    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=False)

        if options['username']:
            users = users.filter(username__in=options['username'])
        try:
            os.mkdir('opinions')
        except:
            pass

        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet('opinions', cell_overwrite_ok=True)
        sheet.write(0, 0, "id")
        sheet.write(0, 1, "teller")
        sheet.write(0, 2, "subject")
        sheet.write(0, 3, "text")
        row = 1

        for user in users:
            opinions = Opinion.objects.filter(teller__user=user)

            for opinion in opinions:
                sheet.write(row, 0, opinion.id)
                sheet.write(row, 1, opinion.teller.get_name())
                sheet.write(row, 2, opinion.subject)
                sheet.write(row, 3, opinion.text)
                row += 1

        name = os.path.join('opinions', 'opinions' + '.xls')
        book.save(name)
        print('OK')
