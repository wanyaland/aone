# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_event_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdiscussion',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
