# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_businessphoto_caption'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='icon',
        ),
        migrations.AddField(
            model_name='parentcategory',
            name='icon',
            field=models.CharField(max_length=40, null=True),
            preserve_default=True,
        ),
    ]
