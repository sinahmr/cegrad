# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-19 10:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TheMost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate', to=settings.AUTH_USER_MODEL)),
                ('the_most', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TheMost')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('voter', 'the_most')]),
        ),
    ]
