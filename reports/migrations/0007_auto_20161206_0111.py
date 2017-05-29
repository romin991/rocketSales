# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-05 18:11
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_report_meta_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='meta_url',
        ),
        migrations.AddField(
            model_name='report',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
