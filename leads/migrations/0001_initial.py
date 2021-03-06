# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-13 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import timelines.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('position', models.CharField(blank=True, max_length=255)),
                ('prof_pic', models.TextField(blank=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('phone', models.TextField(blank=True, max_length=255)),
                ('secondary_phone', models.TextField(blank=True, max_length=255)),
                ('fax', models.TextField(blank=True, max_length=255)),
                ('facebook', models.TextField(blank=True, max_length=255)),
                ('instagram', models.TextField(blank=True, max_length=255)),
                ('twitter', models.TextField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('skype', models.TextField(blank=True, max_length=255)),
                ('line', models.TextField(blank=True, max_length=255)),
                ('mobile_phone', models.TextField(blank=True, max_length=255)),
                ('secondary_mobile_phone', models.TextField(blank=True, max_length=255)),
                ('street', models.TextField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(blank=True, max_length=255)),
                ('pos_code', models.CharField(blank=True, max_length=255)),
                ('lead_source', models.CharField(blank=True, choices=[(b'OFA', b'OfflineAds'), (b'ONA', b'OnlineAds'), (b'IR', b'InternalReferral'), (b'ER', b'ExternalReferral'), (b'P', b'Partner'), (b'S', b'Sales'), (b'TS', b'TradeShow'), (b'SR', b'Seminar')], max_length=3)),
                ('company_name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[(b'O', b'Open'), (b'C', b'Closed'), (b'CV', b'Converted')], default=b'O', max_length=2)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='employees.Employee')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='entities.Entity')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model, timelines.mixins.TimelineMixin),
        ),
    ]
