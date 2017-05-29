from __future__ import unicode_literals

from django.db import models
from datetime import timedelta
from django.utils import timezone
from bases.models import *

class EntityManager(models.Manager):

    def create_entity(self, name, **extra_fields):
        entity = self.model(name=name, **extra_fields)

        entity.save()
        return entity

class Entity(BaseModel):
    name = models.CharField(blank=False, max_length=255)
    industry = models.CharField(blank=True, max_length=255)
    employee_num = models.IntegerField(blank=True, default=0)
    annual_revenue = models.BigIntegerField(blank=True, default=0)
    company_website = models.TextField(blank=True)
    description = models.TextField(blank=True)
    prof_pic = models.TextField(blank=True)

    street = models.TextField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    state = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=255)
    pos_code = models.CharField(blank=True, max_length=255)

    currency = models.CharField(blank=True, default='IDR', max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired = models.DateTimeField(blank=False, null=False)
    max_user = models.IntegerField(blank=False, default=99)

    objects = EntityManager()

    def __unicode__(self):
        return str(self.name)