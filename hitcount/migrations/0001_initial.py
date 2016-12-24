# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('core', '0027_auto_20161224_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ip', models.CharField(max_length=40, editable=False)),
                ('session', models.CharField(max_length=40, editable=False)),
                ('user_agent', models.CharField(max_length=255, editable=False)),
            ],
            options={
                'ordering': ('-created',),
                'get_latest_by': 'created',
                'verbose_name': 'hit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HitCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('object_pk', models.PositiveIntegerField(verbose_name=b'object ID')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-hits',),
                'get_latest_by': 'modified',
                'verbose_name': 'hit count',
                'verbose_name_plural': 'hit counts',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hit',
            name='hitcount',
            field=models.ForeignKey(editable=False, to='hitcount.HitCount'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hit',
            name='user',
            field=models.ForeignKey(editable=False, to='core.Customer', null=True),
            preserve_default=True,
        ),
    ]
