# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 22:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longurl', models.CharField(db_column='long_url', max_length=1024)),
                ('createddate', models.DateField(db_column='created_date', default=datetime.date.today)),
            ],
            options={
                'db_table': 'url',
            },
        ),
    ]
