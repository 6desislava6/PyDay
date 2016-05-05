# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 22:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('from_time', models.TimeField()),
                ('to_time', models.TimeField()),
                ('caption', models.TextField(blank=True)),
                ('importance', models.CharField(choices=[('NO', 'not_important_at_all'), ('SH', 'should_be_done'), ('MI', 'midly_important'), ('I', 'important'), ('VI', 'very_important'), ('EI', 'extremely_important')], default='1', max_length=20)),
                ('coordinates', models.CharField(blank=True, max_length=60)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pyday_calendar.Event')),
                ('participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]