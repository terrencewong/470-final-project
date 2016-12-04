# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 01:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0020_remove_orderedmenuitems_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedmenuitems',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]