# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-31 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Airline', '0014_auto_20170331_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='registrationNumber',
            field=models.CharField(blank=True, default=776707, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='PNR',
            field=models.CharField(default=451474, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='issuedfor',
            name='PNR',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Airline.Ticket', unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='PNR',
            field=models.CharField(blank=True, default='qJ9c2U', max_length=6),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.CharField(default=977, max_length=10),
        ),
    ]