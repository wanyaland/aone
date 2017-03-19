# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20170314_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessphoto',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 18, 11, 51, 6, 270351), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.NewsCategory', null=True),
        ),
    ]
