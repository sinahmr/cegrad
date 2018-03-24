from random import choice
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from main.models import *


@login_required
def question(request):
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
        return HttpResponseRedirect(reverse('question'))
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
    commenter = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        candidate = get_object_or_404(UserProfile, user__username=request.POST.get('candidate'))
        if candidate == commenter:
            return HttpResponseBadRequest('You cannot send comment to yourself')
        text = request.POST.get('text')

        comment_id = request.POST.get('id')
        if comment_id:
            c = Comment.objects.filter(commenter=commenter, id=comment_id).first()
            if not c:
                return HttpResponseBadRequest('You cannot access this comment')
            c.target = candidate
            c.text = text
            c.save()
        else:
            Comment.objects.create(commenter=commenter, target=candidate, text=text)

        return HttpResponseRedirect(reverse('comments'))
    else:
        comment_id = request.GET.get('id')
        if comment_id:
            c = Comment.objects.filter(commenter=commenter, id=comment_id).first()
            if not c:
                return HttpResponseBadRequest('You cannot access this comment')
        else:
            c = None
        candidates = UserProfile.objects.filter(user__is_superuser=False).exclude(user__username=commenter.user.username)
        return render(request, 'main/thought.html', {
            'type': 'comment',
            'item': c,
            'candidates': candidates,
        })


@login_required
def comments(request):
    commenter = request.user
    cs = Comment.objects.filter(commenter__user=commenter)
    for c in cs:
        c.url = reverse('comment') + ('?id=%d' % c.id)
    return render(request, 'main/thoughts.html', {
        'type': 'comment',
        'items': cs
    })


@login_required
def opinion(request):
    teller = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        subject = request.POST.get('subject')
        if not subject:
            return HttpResponseBadRequest('Fill the subject field')
        text = request.POST.get('text')
        opinion_id = request.POST.get('id')
        if opinion_id:
            o = Opinion.objects.filter(teller=teller, id=opinion_id).first()
            if not o:
                return HttpResponseBadRequest('You cannot access this opinion')
            o.subject = subject
            o.text = text
            o.save()
        else:
            Opinion.objects.create(teller=teller, subject=subject, text=text)

        return HttpResponseRedirect(reverse('opinions'))
    else:
        opinion_id = request.GET.get('id')
        if opinion_id:
            o = Opinion.objects.filter(teller=teller, id=opinion_id).first()
            if not o:
                return HttpResponseBadRequest('You cannot access this opinion')
        else:
            o = None
        return render(request, 'main/thought.html', {
            'type': 'opinion',
            'item': o
        })


@login_required
def opinions(request):
    teller = get_object_or_404(UserProfile, user=request.user)
    os = Opinion.objects.filter(teller=teller)
    for o in os:
        o.url = reverse('opinion') + ('?id=%d' % o.id)
    return render(request, 'main/thoughts.html', {
        'type': 'opinion',
        'items': os
    })


def index(request):
    return render(request, 'main/index.html', {})
