# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20170306_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessphoto',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 8, 17, 49, 2, 873000), auto_now_add=True),
        ),
    ]
