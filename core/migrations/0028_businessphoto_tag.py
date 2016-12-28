# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20161224_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessphoto',
            name='tag',
            field=models.CharField(max_length=20, null=True, choices=[(b'H', b'Helpful'), (b'I', b'Inappropriate')]),
            preserve_default=True,
        ),
    ]
