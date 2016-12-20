# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_reviewtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewtag',
            name='ip_address',
            field=models.CharField(max_length=20),
        ),
    ]
