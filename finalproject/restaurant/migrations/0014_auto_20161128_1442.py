# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 22:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_auto_20161127_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedmenuitems',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='orderedmenuitems',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='orderedmenuitems',
            name='num_items',
        ),
        migrations.AlterField(
            model_name='order',
            name='StartTime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 28, 22, 42, 11, 355000, tzinfo=utc)),
        ),
    ]