from django.contrib.auth.models import User
from django.db import models


class TheMost(models.Model):
    title = models.TextField()
    description = models.TextField()


class Vote(models.Model):
    class Meta:
        unique_together = (('voter', 'the_most'),)

    voter = models.ForeignKey(User, related_name='voter')
    candidate = models.ForeignKey(User, related_name='candidate')
    the_most = models.ForeignKey(TheMost)
