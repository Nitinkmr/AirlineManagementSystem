# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-07 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Airline', '0013_auto_20170407_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='registrationNumber',
            field=models.CharField(blank=True, default=108716, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='PNR',
            field=models.CharField(blank=True, default='BhUOa0', max_length=6),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.CharField(default=567, max_length=10),
        ),
    ]
