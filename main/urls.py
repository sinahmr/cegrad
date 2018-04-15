"""cegrad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'q2', views.question2, name='question2'),
    url(r'q', views.question, name='question'),
    url(r'comments', views.comments, name='comments'),
    url(r'comment', views.comment, name='comment'),
    url(r'opinions', views.opinions, name='opinions'),
    url(r'opinion', views.opinion, name='opinion'),
    url(r'votes', views.votes, name='votes'),
    url(r'unvote2', views.unvote2, name='unvote2'),
    url(r'unvote', views.unvote, name='unvote'),
    url(r'login', views.login, name='login'),
    url(r'logout', views.logout, name='logout'),
    url(r'profile$', views.profile, name='profile'),
    url(r'profile/set$', views.set_profile, name='set_profile'),
    url(r'people$', views.people, name='people'),
    url(r'contact$', views.contact, name='contact'),
    url(r'register$', views.register, name='register'),
    url(r'$', views.index, name='home')
]
