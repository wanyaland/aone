# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_event_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user_type',
            field=models.CharField(default=b'B', max_length=20, choices=[(b'C', b'Customer'), (b'B', b'Business')]),
            preserve_default=True,
        ),
    ]
