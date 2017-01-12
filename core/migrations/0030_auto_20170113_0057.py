# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_businessphoto_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessphoto',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 13, 0, 57, 18, 515000), auto_now_add=True),
        ),
    ]
