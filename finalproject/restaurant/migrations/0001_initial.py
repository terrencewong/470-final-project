# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Generated by Django 1.10.2 on 2016-12-05 06:46
=======
# Generated by Django 1.10.2 on 2016-11-27 22:01
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('menu', '0004_choice'),
=======
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Message', models.CharField(max_length=500)),
                ('Resolved', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(max_length=20)),
                ('Table', models.IntegerField(default=0)),
                ('Status', models.CharField(choices=[(b'CREATED', b'Order created'), (b'SENT TO KITCHEN', b'Order sent to kitchen'), (b'STARTED', b'Order started'), (b'READY', b'Order ready to be served'), (b'SERVED', b'Order served'), (b'COMPLETED', b'Order completed')], default=b'CREATED', max_length=15)),
                ('StartTime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
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
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('pay_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Location', models.CharField(max_length=100)),
=======
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(max_length=20)),
                ('Table', models.IntegerField(default=0)),
                ('Status', models.CharField(choices=[(b'CREATED', b'Order created'), (b'SENT TO KITCHEN', b'Order sent to kitchen'), (b'STARTED', b'Order started'), (b'READY', b'Order ready to be served'), (b'SERVED', b'Order served'), (b'COMPLETED', b'Order completed')], default=b'CREATED', max_length=15)),
                ('StartTime', models.DateTimeField(default=django.utils.timezone.now)),
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Table', models.IntegerField(default=0)),
                ('Code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_customer', models.BooleanField(default=True)),
                ('is_kitchen', models.BooleanField(default=False)),
                ('is_server', models.BooleanField(default=False)),
<<<<<<< HEAD
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurant')),
=======
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
<<<<<<< HEAD
            model_name='order',
            name='Restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurant'),
=======
            model_name='menuitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Order'),
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
        ),
        migrations.AddField(
            model_name='alert',
            name='Order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Order'),
        ),
    ]
