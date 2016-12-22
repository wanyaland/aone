# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_review_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('created', models.DateTimeField(default=datetime.datetime(2016, 12, 22, 10, 10, 50, 733000))),
                ('review', models.ForeignKey(related_name=b'reviewviews', to='core.Review')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='review',
            name='session',
        ),
    ]
