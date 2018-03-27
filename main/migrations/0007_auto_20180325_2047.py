# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-25 20:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20180321_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=202)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='about_comment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userprofile', to='main.AboutComment'),
        ),
    ]
