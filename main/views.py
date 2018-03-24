from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import IntegrityError
from django.urls import reverse
from random import choice
from main.models import *
from django.contrib.auth.models import User


# TODO check hidden fields and security

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
        candidates = UserProfile.objects.filter(user__is_superuser=False).exclude(
            user__username=commenter.user.username)
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


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, 'main/login.html', {})
    else:
        return render(request, 'main/login.html', {})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('/login')


@login_required
def profile(request):
    user = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'main/profile.html', {
        'firstname': user.user.first_name,
        'lastname': user.user.last_name
    })


@login_required
def set_profile(request):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == "POST":
        firstName = request.POST.get('first-name')
        lastName = request.POST.get('last-name')
        user.first_name = firstName
        user.last_name = lastName
        user.save()
    try:
        if request.method == 'POST' and request.FILES['profile-photo'] is not None:
            user = get_object_or_404(UserProfile, user=request.user)
            myfile = request.FILES['profile-photo']
            ext = myfile.name.split('.')[-1]
            name = '{}.{}'.format(str(user.user.username), ext)
            name = os.path.join('profiles', name)
            path = settings.MEDIA_ROOT + '/' + name
            if os.path.isfile(path):
                os.remove(path)
            fs = FileSystemStorage()
            filename = fs.save(name, myfile)
            # uploaded_file_url = fs.url(filename)
            user.profile_picture = name
            user.save()
    except KeyError:
        pass
    return redirect('/profile')


def people(request):
    people = UserProfile.objects.filter(user__is_superuser=False)
    return render(request, 'main/people.html', {
        'people': people
    })
