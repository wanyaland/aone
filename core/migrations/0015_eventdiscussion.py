# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_customer_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventDiscussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('date', models.DateField(auto_now=True)),
                ('customer', models.ForeignKey(to='core.Customer')),
                ('event', models.ForeignKey(to='core.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
