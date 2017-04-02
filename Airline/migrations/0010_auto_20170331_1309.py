# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-31 13:09
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Airline', '0009_auto_20170331_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='registrationNumber',
            field=models.CharField(blank=True, default=402560, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='PNR',
            field=models.CharField(default=364427, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='PhoneNumber',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='PNR',
            field=models.CharField(blank=True, default='YhZxZE', max_length=6),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.CharField(default=505, max_length=10),
        ),
    ]