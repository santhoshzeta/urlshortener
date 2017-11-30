# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 02:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortenerapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='createddate',
        ),
        migrations.AddField(
            model_name='url',
            name='createddatetime',
            field=models.DateTimeField(db_column='created_datetime', default=datetime.date.today),
        ),
    ]
