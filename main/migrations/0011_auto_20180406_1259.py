# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-06 08:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20180406_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote2',
            name='the_most',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.TheMost2'),
        ),
    ]
