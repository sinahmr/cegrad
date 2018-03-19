from random import choice

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

from main.models import *


@login_required
def question(request):
    voter = request.user
    if request.method == 'POST':
        candidate = get_object_or_404(User, username=request.POST.get('candidate'))
        q = get_object_or_404(TheMost, pk=request.POST.get('question_id'))
        try:
            Vote.objects.create(voter=voter, candidate=candidate, the_most=q)
        except IntegrityError:
            return HttpResponseBadRequest('You have already voted')
        return HttpResponseRedirect(request.path)
    else:
        remaining_questions = TheMost.objects.exclude(vote__voter=voter)
        if remaining_questions.count() > 0:
            chosen_question = choice(remaining_questions)
        else:
            chosen_question = None

        candidates = User.objects.filter(is_superuser=False).exclude(username=voter.username)
        return render(request, 'main/question.html', {
            'question': chosen_question,
            'candidates': candidates,
        })

