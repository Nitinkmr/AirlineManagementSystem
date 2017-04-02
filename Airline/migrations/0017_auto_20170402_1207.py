# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-02 12:07
from __future__ import unicode_literals

import Airline.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Airline', '0016_auto_20170402_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='registrationNumber',
            field=models.CharField(blank=True, default=138569, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='PNR',
            field=models.CharField(default=881456, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='Email',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='PhoneNumber',
            field=models.CharField(max_length=10, unique=True, validators=[Airline.models.verifyPhoneNo]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='PNR',
            field=models.CharField(blank=True, default='X91MIC', max_length=6),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.CharField(default=878, max_length=10),
        ),
    ]