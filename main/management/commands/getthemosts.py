import operator

from django.core.management.base import BaseCommand
from main.models import *
import xlwt
import os


class Command(BaseCommand):
    help = "Change users' password to something random and send email to them"

    def add_arguments(self, parser):
        parser.add_argument('the_mosts', nargs='*', type=str, default=None)

    def handle(self, *args, **options):
        the_mosts = TheMost.objects.all()

        try:
            os.mkdir('the_most')
        except:
            pass

        for the_most in the_mosts:
            votes = Vote.objects.filter(the_most=the_most).order_by('candidate')
            if votes:
                book = xlwt.Workbook(encoding="utf-8")
                sheet = book.add_sheet(the_most.text.replace('\u200c', ' '), cell_overwrite_ok=True)
                sheet.write(0, 0, "#")
                sheet.write(0, 1, "The Most")
                sheet.write(0, 2, "Candidate")
                sheet.write(0, 3, "Vote Id")

                votes_dic = {}
                for i, vote in enumerate(votes):
                    try:
                        candidate = vote.candidate.get_name()
                    except:
                        candidate = '-'

                    if candidate in votes_dic:
                        votes_dic[candidate] += 1
                    else:
                        votes_dic[candidate] = 1

                votes_dic = reversed(sorted(votes_dic.items(), key=operator.itemgetter(1)))

                row = 1
                for key, value in votes_dic:
                    sheet.write(row, 0, row)
                    sheet.write(row, 1, the_most.text)
                    sheet.write(row, 2, key)
                    sheet.write(row, 3, value)
                    row += 1

                name = os.path.join('the_most', the_most.text.replace('\u200c', ' ') + '.xls')
                book.save(name)

        the_mosts = TheMost2.objects.all()
        for the_most in the_mosts:
            votes = Vote2.objects.filter(the_most=the_most).order_by('candidate')
            if votes:
                book = xlwt.Workbook(encoding="utf-8")
                sheet = book.add_sheet(the_most.text.replace('\u200c', ' '), cell_overwrite_ok=True)
                sheet.write(0, 0, "#")
                sheet.write(0, 1, "The Most")
                sheet.write(0, 2, "Candidate")
                sheet.write(0, 3, "Vote Id")

                votes_dic = {}
                for i, vote in enumerate(votes):
                    try:
                        candidate = vote.candidate.get_name()
                    except:
                        candidate = '-'

                    if candidate in votes_dic:
                        votes_dic[candidate] += 1
                    else:
                        votes_dic[candidate] = 1

                votes_dic = reversed(sorted(votes_dic.items(), key=operator.itemgetter(1)))

                row = 1
                for key, value in votes_dic:
                    sheet.write(row, 0, row)
                    sheet.write(row, 1, the_most.text)
                    sheet.write(row, 2, key)
                    sheet.write(row, 3, value)
                    row += 1

                name = os.path.join('the_most', the_most.text.replace('\u200c', ' ') + '.xls')
                book.save(name)
        print('OK')
