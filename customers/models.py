from __future__ import unicode_literals

from django.db import models
from employees.models import *
from companies.models import *
from django.contrib.contenttypes.fields import GenericRelation
from tasks.models import *
from events.models import *
from notes.models import *
from timelines.mixins import *
from timelines.models import *
from leads.models import *
import time

# Create your models here.

class CustomerManager(models.Manager):

    def create_customer(self, first_name, entity, employee, **extra_fields):
        customer = self.model(first_name=first_name, entity=entity, employee=employee, **extra_fields)

        customer.save()

        return customer


class Customer(BaseCoreModel, ContactInfoMixin, ContactContactMixin, AddressMixin, TimelineMixin):

    #Cannot use member because entity should always exist
    entity = models.ForeignKey(Entity, related_name='customers')
    employee = models.ForeignKey(Employee, related_name='customers')
    company = models.ForeignKey(Company, related_name='customers')

    tasks = GenericRelation(Task, content_type_field='contact_ct', object_id_field='contact_id', related_query_name='customer')
    events = GenericRelation(Event, content_type_field='contact_ct', object_id_field='contact_id')
    notes = GenericRelation(Note)

    lead_origin = models.OneToOneField(Lead, related_name='converted_customer', null=True, blank=True)
    timeline = GenericRelation(Timeline)

    objects = CustomerManager()

    def __unicode__(self):
        return str(self.first_name) + ' ' + str(self.entity) + ' ' + str(self.employee) + ' ' + str(self.company)

    def active_deals(self):
        return self.deals.filter(is_deleted=False)

    def active_tasks(self):
        return self.tasks.filter(is_deleted=False)

    def active_events(self):
        return self.events.filter(is_deleted=False)

    def active_notes(self):
        return self.notes.filter(is_deleted=False)

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
        return str(self.first_name)

    def get_epoch_created_at(self):
        return int(time.mktime(self.created_at.timetuple()))

    class Meta:
        ordering = ['-created_at']