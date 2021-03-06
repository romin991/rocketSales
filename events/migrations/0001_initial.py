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
        ('companies', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('deals', '0001_initial'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('street', models.TextField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(blank=True, max_length=255)),
                ('pos_code', models.CharField(blank=True, max_length=255)),
                ('start_time', models.DateTimeField(db_index=True)),
                ('duration', models.IntegerField()),
                ('contact_id', models.UUIDField()),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='companies.Company')),
                ('contact_ct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('deal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='deals.Deal')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='employees.Employee')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='entities.Entity')),
            ],
            options={
                'ordering': ['start_time', '-created_at'],
            },
            bases=(models.Model, timelines.mixins.TimelineMixin),
        ),
    ]
