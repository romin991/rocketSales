# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-13 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.TextField()),
                ('object_id', models.UUIDField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='employees.Employee')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='entities.Entity')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
