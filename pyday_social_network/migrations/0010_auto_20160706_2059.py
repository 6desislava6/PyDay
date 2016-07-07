# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-06 17:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pyday_social_network', '0009_auto_20160706_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pydayuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 6, 17, 59, 33, 949321, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pydayuser',
            name='picture',
            field=models.FileField(default='/media/pictures/generic_profile_photo.png', upload_to='pictures/'),
        ),
    ]
