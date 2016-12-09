# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_auto_20161208_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.IntegerField()),
                ('tag', models.CharField(max_length=20, choices=[(b'C', b'COOL'), (b'H', b'HELPFUL'), (b'F', b'FUNNY')])),
                ('date_added', models.DateField(default=datetime.datetime.now, editable=False)),
                ('date_changed', models.DateField(default=datetime.datetime.now, editable=False)),
                ('cookie', models.CharField(max_length=32, null=True, blank=True)),
                ('review', models.OneToOneField(to='core.Review')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
