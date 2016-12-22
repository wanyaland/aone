# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20161219_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewtag',
            name='review',
            field=models.ForeignKey(to='core.Review'),
        ),
    ]
