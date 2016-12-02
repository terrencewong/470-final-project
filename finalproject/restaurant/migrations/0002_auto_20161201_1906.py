# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Location', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='Status',
            field=models.CharField(choices=[('CREATED', 'Order created'), ('SENT TO KITCHEN', 'Order sent to kitchen'), ('STARTED', 'Order started'), ('READY', 'Order ready to be served'), ('SERVED', 'Order served'), ('COMPLETED', 'Order completed')], default='CREATED', max_length=15),
        ),
    ]
