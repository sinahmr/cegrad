#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
from django.db import models
from main.storage import OverwriteStorage


def image_path(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(str(instance.user.username), ext)
    return os.path.join('profiles', name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(max_length=100, storage=OverwriteStorage(), upload_to=image_path, blank=True)

    def get_name(self):
        if self.user.first_name or self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name
        return self.user.username


class TheMost(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Vote(models.Model):
    class Meta:
        unique_together = (('voter', 'the_most'),)

    voter = models.ForeignKey(UserProfile, related_name='voter')
    candidate = models.ForeignKey(UserProfile, related_name='candidate')
    the_most = models.ForeignKey(TheMost)


class Comment(models.Model):
    commenter = models.ForeignKey(UserProfile, related_name='commenter')
    target = models.ForeignKey(UserProfile, related_name='target', verbose_name='نظرگیرنده')
    text = models.TextField(verbose_name='متن نظر')


class Opinion(models.Model):
    teller = models.ForeignKey(UserProfile)
    subject = models.CharField(max_length=1000)
    text = models.TextField()
