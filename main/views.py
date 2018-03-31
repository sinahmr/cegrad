from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import IntegrityError
from django.urls import reverse
from random import choice, randint
from main.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from itertools import chain
from PIL import Image


@login_required
def question(request):
    voter = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        candidate_username = request.POST.get('candidate')
        if candidate_username == 'null':
            candidate = None
        else:
            candidate = get_object_or_404(UserProfile, user__username=candidate_username)
            if candidate == voter:
                messages.error(request, 'نمی‌تونی به خودت رای بدی!')
                return redirect('question')
        q = get_object_or_404(TheMost, pk=request.POST.get('question_id'))
        try:
            Vote.objects.create(voter=voter, candidate=candidate, the_most=q)
        except IntegrityError:
            messages.error(request, 'به این مورد قبلا رای داده بودی، ممکنه دوبار بعدی رو زده باشی!')
            return redirect('question')
        return HttpResponseRedirect(reverse('question'))
    else:
        remaining_questions = TheMost.objects.exclude(vote__voter=voter)
        remaining_count = remaining_questions.count()
        if remaining_count > 0:
            chosen_question = choice(remaining_questions)
        else:
            chosen_question = None

        candidates = UserProfile.objects.filter(user__is_superuser=False).exclude(
            user__username=voter.user.username).order_by('?')
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
            messages.error(request, 'نمی‌تونی برای خودت نظر بفرستی')
            return redirect('comment')
        text = request.POST.get('text')

        comment_id = request.POST.get('id')
        if comment_id != 'None' and comment_id:
            c = Comment.objects.filter(commenter=commenter, id=comment_id).first()
            if not c:
                messages.error(request, 'به این نظر دسترسی نداری!')
                return redirect('comments')
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
                messages.error(request, 'به این نظر دسترسی نداری!')
                return redirect('comments')
        else:
            to = request.GET.get('to')
            if to:
                to_profile = get_object_or_404(UserProfile, user__username=to)
                c = Comment(target=to_profile)
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
            messages.error(request, 'عنوان رو پر نکردی!')
            return redirect('opinion')
        text = request.POST.get('text')
        opinion_id = request.POST.get('id')
        if opinion_id:
            o = Opinion.objects.filter(teller=teller, id=opinion_id).first()
            if not o:
                messages.error(request, 'به این نظر دسترسی نداری!')
                return redirect('opinions')
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
                messages.error(request, 'به این نظر دسترسی نداری!')
                return redirect('opinions')
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
            next = request.GET.get('next')
            auth_login(request, user)
            messages.success(request, 'خوش اومدی!')
            if next:
                return redirect(next)
            else:
                return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
            return render(request, 'main/login.html', {})
    else:
        return render(request, 'main/login.html', {})


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'خسته نباشی! اگه بازم خواستی به کسی نظر بدی یا نظراتو ویرایش کنی برگرد!')
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
            name = '{}-{}.{}'.format(str(user.user.username), randint(0, 100000), ext)
            name = os.path.join('profiles', name)
            path = settings.MEDIA_ROOT + '/' + name
            old_path = settings.BASE_DIR + '/' + user.profile_picture.url
            # second condition is to not delete default photos!
            if os.path.isfile(old_path) and 'profiles' in user.profile_picture.url.split('/'):
                os.remove(old_path)
            crop_info = request.POST.get('crop')
            crop_info = crop_info.split(',')
            im = Image.open(request.FILES['profile-photo'])
            im = im.crop((float(crop_info[0]), float(crop_info[1]), float(crop_info[0]) + float(crop_info[2]),
                          float(crop_info[1]) + float(crop_info[3])))
            im.save(path)
            # fs = FileSystemStorage()
            # filename = fs.save(name, myfile)
            # uploaded_file_url = fs.url(filename)
            user.profile_picture = name
            user.save()
    except KeyError:
        pass
    return redirect('profile')


def people(request):
    people = UserProfile.objects.filter(user__is_superuser=False).order_by('user__last_name')
    return render(request, 'main/people.html', {
        'people': people
    })


def contact(request):
    return render(request, 'main/contact.html', {})