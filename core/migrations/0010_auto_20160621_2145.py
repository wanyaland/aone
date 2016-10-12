# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_business_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField()),
                ('opening_hours', models.FloatField()),
                ('closing_hours', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='business',
            name='business_hours',
            field=models.ManyToManyField(to='core.BusinessHours'),
            preserve_default=True,
        ),
    ]
