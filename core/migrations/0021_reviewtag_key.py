# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20161220_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewtag',
            name='key',
            field=models.CharField(max_length=32, null=True),
            preserve_default=True,
        ),
    ]
