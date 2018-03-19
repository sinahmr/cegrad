from random import choice

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from main.models import TheMost


@login_required
def question(request):
    voter = request.user
    if request.method == 'POST':
        pass
    else:
        remaining_questions = TheMost.objects.exclude(vote__voter=voter)
        chosen_question = choice(remaining_questions)

        candidates = User.objects.filter(is_superuser=False).exclude(username=voter.username)
        return render(request, 'main/question.html')

