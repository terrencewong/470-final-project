# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-13 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20161113_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Completed',
            field=models.BooleanField(default=0),
        ),
    ]
