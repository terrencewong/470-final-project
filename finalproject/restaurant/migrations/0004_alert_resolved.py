# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20161127_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='Resolved',
            field=models.BooleanField(default=0),
        ),
    ]
