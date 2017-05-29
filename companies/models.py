from __future__ import unicode_literals

from django.db import models
from employees.models import *
from django.contrib.contenttypes.fields import GenericRelation
from tasks.models import *
from notes.models import *
from deals.constants import *
from timelines.mixins import *
from timelines.models import *
from django.utils import timezone

import time

class CompanyManager(models.Manager):

    def create_company(self, name, entity, employee, **extra_fields):
        company = self.model(name=name, entity=entity, employee=employee, **extra_fields)

        company.save()

        return company

# Create your models here.
class Company(BaseCoreModel, CompanyInfoMixin, CompanyContactMixin, AddressMixin, ShippingAddressMixin, TimelineMixin):

    #Cannot use member because entity should always exist
    entity = models.ForeignKey(Entity, related_name='companies')
    employee = models.ForeignKey(Employee, related_name='companies')

    notes = GenericRelation(Note)

    timeline = GenericRelation(Timeline)

    objects = CompanyManager()

    def __unicode__(self):
        return str(self.name) + ' ' + str(self.entity) + ' ' + str(self.employee)

    def active_deals(self):
        return self.deals.filter(is_deleted=False)

    def active_tasks(self):
        return self.tasks.filter(is_deleted=False)

    def active_events(self):
        return self.events.filter(is_deleted=False)

    def active_notes(self):
        return self.notes.filter(is_deleted=False)

    def active_customers(self):
        return self.customers.filter(is_deleted=False)

    def active_open_deals(self):
        return self.active_deals().filter(status=DealConstant.OPEN)

    def active_closed_deals(self):
        return self.active_deals().filter(status=DealConstant.CLOSED)

    def active_open_tasks(self):
        return self.active_tasks().filter(status=TaskConstant.OPEN)

    def active_closed_tasks(self):
        return self.active_tasks().filter(status=TaskConstant.CLOSED)

    def active_open_events(self):
        return self.active_events().filter(start_time__gte=timezone.now()).order_by('start_time')

    def active_closed_events(self):
        return self.active_events().filter(start_time__lte=timezone.now()).order_by('-start_time')

    def get_timeline_title(self):
        return str(self.name)

    def get_epoch_created_at(self):
        return int(time.mktime(self.created_at.timetuple()))

    class Meta:
        ordering = ['-created_at']