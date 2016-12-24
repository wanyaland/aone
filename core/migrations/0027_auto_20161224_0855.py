# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20161222_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessview',
            name='business',
        ),
        migrations.DeleteModel(
            name='BusinessView',
        ),
        migrations.RemoveField(
            model_name='eventview',
            name='event',
        ),
        migrations.DeleteModel(
            name='EventView',
        ),
        migrations.RemoveField(
            model_name='modelview',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='ModelView',
        ),
        migrations.RemoveField(
            model_name='reviewview',
            name='review',
        ),
        migrations.DeleteModel(
            name='ReviewView',
        ),
    ]
