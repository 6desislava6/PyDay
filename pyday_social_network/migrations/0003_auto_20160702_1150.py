# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-02 11:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pyday_social_network', '0002_auto_20160702_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pydayuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 2, 11, 50, 30, 770082, tzinfo=utc)),
        ),
    ]
