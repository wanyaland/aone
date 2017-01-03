# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_businessphoto_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessphoto',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 3, 3, 5, 16, 100000), auto_now_add=True),
            preserve_default=True,
        ),
    ]
