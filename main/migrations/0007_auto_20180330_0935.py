# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20180321_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.ForeignKey(related_name='target', verbose_name=b'\xd9\x86\xd8\xb8\xd8\xb1\xda\xaf\xdb\x8c\xd8\xb1\xd9\x86\xd8\xaf\xd9\x87', to='main.UserProfile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name=b'\xd9\x85\xd8\xaa\xd9\x86 \xd9\x86\xd8\xb8\xd8\xb1'),
        ),
    ]
