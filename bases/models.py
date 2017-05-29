from __future__ import unicode_literals

from django.db import models
from bases.constants import *
import uuid

# Create your models here.
class BaseCoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    global_last_changed = models.DateTimeField(blank=False, null=False)

    class Meta:
        abstract = True

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ContactInfoMixin(models.Model):
    first_name = models.CharField(blank=False, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    title = models.CharField(blank=True, max_length=255)
    position = models.CharField(blank=True, max_length=255)
    prof_pic = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

class CompanyInfoMixin(models.Model):
    name = models.CharField(blank=False, max_length=255)
    industry = models.CharField(blank=True, max_length=255)
    employee_num = models.IntegerField(blank=True, default=0)
    annual_revenue = models.BigIntegerField(blank=True, default=0)
    company_website = models.TextField(blank=True)
    description = models.TextField(blank=True)
    prof_pic = models.TextField(blank=True)

    class Meta:
        abstract = True

class BaseContactMixin(models.Model):
    phone = models.TextField(blank=True, max_length=255)
    secondary_phone = models.TextField(blank=True, max_length=255)
    fax = models.TextField(blank=True, max_length=255)
    facebook = models.TextField(blank=True, max_length=255)
    instagram = models.TextField(blank=True, max_length=255)
    twitter = models.TextField(blank=True, max_length=255)

    class Meta:
        abstract = True

class ContactContactMixin(BaseContactMixin):
    email = models.EmailField(blank=True, null=True)
    skype = models.TextField(blank=True, max_length=255)
    line = models.TextField(blank=True, max_length=255)
    mobile_phone = models.TextField(blank=True, max_length=255)
    secondary_mobile_phone = models.TextField(blank=True, max_length=255)

    class Meta:
        abstract = True

class CompanyContactMixin(BaseContactMixin):
    email = models.EmailField(blank=True, null=True)
    
    class Meta:
        abstract = True

class AddressMixin(models.Model):
    street = models.TextField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    state = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=255)
    pos_code = models.CharField(blank=True, max_length=255)

    class Meta:
        abstract = True

class ShippingAddressMixin(models.Model):
    shipping_street = models.TextField(blank=True, max_length=255)
    shipping_city = models.CharField(blank=True, max_length=255)
    shipping_state = models.CharField(blank=True, max_length=255)
    shipping_country = models.CharField(blank=True, max_length=255)
    shipping_pos_code = models.CharField(blank=True, max_length=255)

    class Meta:
        abstract = True
