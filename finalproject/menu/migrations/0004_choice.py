# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 02:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_survey'),
    ]

    operations = [
        migrations.CreateModel(
            name='choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.survey')),
            ],
        ),
    ]
