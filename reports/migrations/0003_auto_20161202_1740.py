# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-02 10:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20161202_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='start_date',
            field=models.DateField(),
        ),
    ]