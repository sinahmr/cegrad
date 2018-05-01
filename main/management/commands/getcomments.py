from django.core.management.base import BaseCommand
from main.models import *
import xlwt
import os


class Command(BaseCommand):
    help = "Change users' password to something random and send email to them"

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='*', type=str, default=None)

    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=False)

        if options['username']:
            users = users.filter(username__in=options['username'])
        try:
            os.mkdir('comments')
        except:
            pass
        for user in users:
            comments = Comment.objects.filter(target__user=user, show=True)
            if comments:
                book = xlwt.Workbook(encoding="utf-8")
                sheet = book.add_sheet(user.username, cell_overwrite_ok=True)
                sheet.write(0, 0, "id")
                sheet.write(0, 1, "commenter")
                sheet.write(0, 2, "target")
                sheet.write(0, 3, "text")

                for i, comment in enumerate(comments):
                    sheet.write(i+1, 0, comment.id)
                    sheet.write(i+1, 1, comment.commenter.get_name())
                    sheet.write(i+1, 2, comment.target.get_name())
                    sheet.write(i+1, 3, comment.text)
                    # print(comment.id, comment.commenter.get_name())
                name = os.path.join('comments', user.username + '.xls')
                book.save(name)
        print('OK')
