from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import TheMost


@login_required
def question(request):
    voter = request.user
    a = TheMost.objects.filter(vote__voter=voter)
    print(a)
    return render('<div/>')
