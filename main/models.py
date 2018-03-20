from django.contrib.auth.models import User
from django.db import models


def get_name(self):
    if self.first_name or self.last_name:
        return self.first_name + ' ' + self.last_name
    return self.username

User.add_to_class('get_name', get_name)


class TheMost(models.Model):
    text = models.TextField()


class Vote(models.Model):
    class Meta:
        unique_together = (('voter', 'the_most'),)

    voter = models.ForeignKey(User, related_name='voter')
    candidate = models.ForeignKey(User, related_name='candidate')
    the_most = models.ForeignKey(TheMost)


class Comment(models.Model):
    commenter = models.ForeignKey(User, related_name='commenter')
    target = models.ForeignKey(User, related_name='target', verbose_name='نظرگیرنده')
    text = models.TextField(verbose_name='متن نظر')


class Opinion(models.Model):
    teller = models.ForeignKey(User)
    subject = models.CharField(max_length=1000)
    text = models.TextField()
