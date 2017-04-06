# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-06 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Airline', '0003_auto_20170406_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passenger',
            old_name='PNR',
            new_name='pnrNo',
        ),
        migrations.AlterField(
            model_name='aircraft',
            name='registrationNumber',
            field=models.CharField(blank=True, default=38874, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='PNR',
            field=models.CharField(blank=True, default='3COFO2', max_length=6),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.CharField(default=115, max_length=10),
        ),
    ]