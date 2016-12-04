# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 07:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedMenuItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_items', models.IntegerField(default=0)),
                ('notes', models.TextField(max_length=500, null=True)),
                ('item_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.menu')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Order')),
            ],
        ),
    ]