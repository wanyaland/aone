# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20161222_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('created', models.DateTimeField(default=datetime.datetime(2016, 12, 22, 21, 16, 15, 296000))),
                ('event', models.ForeignKey(to='core.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='businessview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 21, 16, 15, 293000)),
        ),
        migrations.AlterField(
            model_name='modelview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 21, 16, 15, 300000)),
        ),
        migrations.AlterField(
            model_name='reviewview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 21, 16, 15, 291000)),
        ),
    ]
