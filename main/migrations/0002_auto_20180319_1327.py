# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-19 13:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='themost',
            old_name='description',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='themost',
            name='title',
        ),
    ]
