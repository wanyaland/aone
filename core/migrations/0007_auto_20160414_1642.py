# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160413_0232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='location',
        ),
        migrations.AddField(
            model_name='business',
            name='latitude',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='business',
            name='longitude',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
