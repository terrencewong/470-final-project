# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedmenuitems',
            name='timestamp',
            field=models.TimeField(auto_now=True),
        ),
    ]
