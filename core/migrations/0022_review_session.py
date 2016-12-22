# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_reviewtag_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='session',
            field=models.CharField(max_length=40, null=True),
            preserve_default=True,
        ),
    ]
