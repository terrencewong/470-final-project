# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='specialmenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Description', models.CharField(max_length=200)),
                ('Nutrition', models.CharField(max_length=200)),
                ('Price', models.IntegerField(default=170)),
            ],
        ),
    ]
