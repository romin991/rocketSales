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
        ('customers', '0001_initial'),
        ('employees', '0001_initial'),
        ('companies', '0001_initial'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('expected_revenue', models.BigIntegerField(blank=True, default=0)),
                ('expected_closing_date', models.DateField(blank=True, null=True)),
                ('closing_revenue', models.BigIntegerField(blank=True, default=0)),
                ('lost_note', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[(b'O', b'Open'), (b'P', b'Progress'), (b'CW', b'ClosedWon'), (b'CL', b'ClosedLost')], default=b'O', max_length=2)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='companies.Company')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='customers.Customer')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='employees.Employee')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='entities.Entity')),
            ],
            options={
                'ordering': ['expected_closing_date', '-created_at'],
            },
            bases=(models.Model, timelines.mixins.TimelineMixin),
        ),
    ]
