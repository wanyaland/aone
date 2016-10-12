# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner_photo', models.ImageField(null=True, upload_to=b'businesses/banner/%Y/%m/%d')),
                ('popularity_rating', models.IntegerField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('phone_number', models.TextField(null=True, blank=True)),
                ('web_address', models.URLField(null=True)),
                ('photo', models.ImageField(null=True, upload_to=b'businesses/%Y/%m/%d')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('location', geoposition.fields.GeopositionField(max_length=42, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=75, null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('description', models.TextField(null=True)),
                ('price_range', models.IntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BusinessPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=b'businesses/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('parent_category', models.ForeignKey(blank=True, to='core.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.FileField(null=True, upload_to=b'avatars/%Y/%m/%d', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True)),
                ('event_date', models.DateTimeField(null=True)),
                ('where', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(null=True)),
                ('website_url', models.URLField(null=True)),
                ('price', models.IntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('rating_votes', models.PositiveIntegerField(default=0, editable=False, blank=True)),
                ('rating_score', models.IntegerField(default=0, editable=False, blank=True)),
                ('business', models.ForeignKey(to='core.Business', null=True)),
                ('customer', models.ForeignKey(to='core.Customer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='categories',
            field=models.ManyToManyField(to='core.EventCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='businessphoto',
            name='review',
            field=models.ForeignKey(to='core.Review', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='business',
            name='categories',
            field=models.ManyToManyField(to='core.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='business',
            name='country',
            field=models.ForeignKey(to='core.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='business',
            name='features',
            field=models.ManyToManyField(to='core.Features', null=True),
            preserve_default=True,
        ),
    ]
