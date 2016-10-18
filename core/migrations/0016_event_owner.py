# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_eventdiscussion'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.OneToOneField(null=True, to='core.Customer'),
            preserve_default=True,
        ),
    ]
