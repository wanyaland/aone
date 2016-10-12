# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20160621_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessphoto',
            name='photo_type',
            field=models.CharField(max_length=20, null=True, choices=[(b'BP', b'BusinessPhoto'), (b'RP', b'ReviewPhoto'), (b'UP', b'UserPhoto')]),
        ),
    ]
