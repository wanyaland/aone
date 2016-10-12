# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_category_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessphoto',
            name='review',
        ),
        migrations.AddField(
            model_name='businessphoto',
            name='business',
            field=models.ForeignKey(to='core.Business', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='businessphoto',
            name='photo_type',
            field=models.CharField(max_length=20, null=True, choices=[(b'BP', b'BusinessPhoto'), (b'RP', b'ReviewPhoto')]),
            preserve_default=True,
        ),
    ]
