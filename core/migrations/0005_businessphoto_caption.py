# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160406_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessphoto',
            name='caption',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
