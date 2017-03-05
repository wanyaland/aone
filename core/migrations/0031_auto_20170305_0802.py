# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20170113_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessphoto',
            name='review',
            field=models.ForeignKey(to='core.Review', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='businessphoto',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 5, 8, 2, 35, 456000), auto_now_add=True),
        ),
    ]
