# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-02 08:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pyday_social_network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pydayuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 2, 8, 29, 54, 961379, tzinfo=utc)),
        ),
    ]