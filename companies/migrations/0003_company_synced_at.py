# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-15 08:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20161114_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='synced_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 15, 8, 59, 3, 37211, tzinfo=utc)),
            preserve_default=False,
        ),
    ]