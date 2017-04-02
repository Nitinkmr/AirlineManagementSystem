# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-02 11:48
from __future__ import unicode_literals

import Airline.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Airline', '0015_auto_20170331_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='registrationNumber',
            field=models.CharField(blank=True, default=873097, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='PNR',
            field=models.CharField(default=972228, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='Email',
            field=models.CharField(max_length=30, unique=True, validators=[Airline.models.verify_email]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='PNR',
            field=models.CharField(blank=True, default='yLm0zx', max_length=6),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.CharField(default=857, max_length=10),
        ),
    ]