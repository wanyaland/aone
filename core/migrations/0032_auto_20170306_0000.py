# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20170305_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessphoto',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 6, 0, 0, 17, 338000), auto_now_add=True),
        ),
    ]
