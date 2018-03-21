from random import choice

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

from main.models import *


# TODO check hidden fields and security

@login_required
def question(request):
    # voter = request.user
    voter = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        candidate = get_object_or_404(UserProfile, user__username=request.POST.get('candidate'))
        if candidate == voter:
            return HttpResponseBadRequest('You cannot vote yourself')
        q = get_object_or_404(TheMost, pk=request.POST.get('question_id'))
        try:
            Vote.objects.create(voter=voter, candidate=candidate, the_most=q)
        except IntegrityError:
            return HttpResponseBadRequest('You have already voted')
        return HttpResponseRedirect(request.path)
    else:
        remaining_questions = TheMost.objects.exclude(vote__voter=voter)
        remaining_count = remaining_questions.count()
        if remaining_count > 0:
            chosen_question = choice(remaining_questions)
        else:
            chosen_question = None

        candidates = UserProfile.objects.filter(user__is_superuser=False).exclude(user__username=voter.user.username)
        return render(request, 'main/question.html', {
            'question': chosen_question,
            'candidates': candidates,
            'voted_count': TheMost.objects.filter(vote__voter=voter).count(),
            'remaining_count': remaining_count
        })


@login_required
def comment(request):
    commenter = request.user
    commenter = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        candidate = get_object_or_404(UserProfile, user__username=request.POST.get('candidate'))
        if candidate == commenter:
            return HttpResponseBadRequest('You cannot send comment to yourself')
        text = request.POST.get('text')

        comment_id = request.POST.get('comment_id')
        if comment_id:
            c = Comment.objects.filter(commenter=commenter, id=comment_id).first()
            if not c:
                return HttpResponseBadRequest('You cannot access this comment')
            c.target = candidate
            c.text = text
            c.save()
        else:
            Comment.objects.create(commenter=commenter, target=candidate, text=text)

        return HttpResponseRedirect(request.path)  # TODO redirect to comments list page
    else:
        comment_id = request.GET.get('comment_id')
        if comment_id:
            c = Comment.objects.filter(commenter=commenter, id=comment_id).first()
            if not c:
                return HttpResponseBadRequest('You cannot access this comment')
        else:
            c = None
        candidates = UserProfile.objects.filter(user__is_superuser=False).exclude(user__username=commenter.user.username)
        return render(request, 'main/comment.html', {
            'comment': c,
            'candidates': candidates,
        })
