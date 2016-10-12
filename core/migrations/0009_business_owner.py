 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_business_claimed'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='owner',
            field=models.ForeignKey(to='core.Customer', null=True),
            preserve_default=True,
        ),
    ]
