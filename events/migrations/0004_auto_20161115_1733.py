# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-15 10:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_synced_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='synced_at',
            new_name='global_last_changed',
        ),
    ]
