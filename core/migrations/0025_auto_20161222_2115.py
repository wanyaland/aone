# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20161222_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 21, 15, 54, 972000)),
        ),
        migrations.AlterField(
            model_name='modelview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 21, 15, 54, 972000)),
        ),
        migrations.AlterField(
            model_name='reviewview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 21, 15, 54, 972000)),
        ),
    ]
