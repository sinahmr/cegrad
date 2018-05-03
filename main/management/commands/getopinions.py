from django.core.management.base import BaseCommand
from main.models import *
import xlwt
import os
import re

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

        for user in users:
            opinions = Opinion.objects.filter(teller__user=user)
            if opinions:
                book = xlwt.Workbook(encoding="utf-8")
                sheet = book.add_sheet(user.username, cell_overwrite_ok=True)
                sheet.write(0, 0, "id")
                sheet.write(0, 1, "teller")
                sheet.write(0, 2, "subject")
                sheet.write(0, 3, "text")

                for i, opinion in enumerate(opinions):
                    sheet.write(i+1, 0, opinion.id)
                    sheet.write(i+1, 1, opinion.teller.get_name())
                    sheet.write(i+1, 2, f2(f3(f1(f4(opinion.text)))))
                    sheet.write(i+1, 3, f2(f3(f1(f4(opinion.text)))))

                name = os.path.join('opinions', user.username + '.xls')
                book.save(name)
        print('OK')


def f1(input):
    output = input
    pattern = '\^_+\^'
    for x in set(re.findall(pattern, input, re.MULTILINE)):
        y = '\lstinline!%s!' % x
        output = output.replace(x, y)
    return output


def f2(input):
    output = input
    pattern = '\n'
    for x in set(re.findall(pattern, input, re.MULTILINE)):
        y = r' \newline '
        output = output.replace(x, y)
    return output


def f3(input):
    output = input.replace('#', '\#').replace("@", "\@").replace("&", "\&").replace("$", "\$").replace("~", r"\textasciitilde ")
    return output


def f4(input):
    output = input
    pattern = '([a-zA-Z\d,#?]+[a-zA-Z\d,\s,<>,.;:!?@#$_$)(]*[a-zA-Z\d,\s,:,.!?)(]+)'
    for x in set(re.findall(pattern, input, re.MULTILINE)):
        y = '\lr{ %s }' % x
        output = output.replace(x, y)
    return output
