from __future__ import unicode_literals

from django.db import models
from employees.models import *
from django.contrib.contenttypes.fields import GenericRelation
from tasks.models import *
from events.models import *
from notes.models import *
from timelines.mixins import *
from timelines.models import *
from leads.constants import *
import time

class LeadManager(models.Manager):

    def create_lead(self, first_name, entity, employee, **extra_fields):
        lead = self.model(first_name=first_name, entity=entity, employee=employee, **extra_fields)

        lead.save()

        return lead


# Create your models here.
class Lead(BaseCoreModel, ContactInfoMixin, ContactContactMixin, AddressMixin, TimelineMixin):
    lead_source = models.CharField(max_length=3, choices=ContactConstant.LEAD_SOURCE, blank=True, db_index=True)
    company_name = models.CharField(max_length=255)
    status = models.CharField(max_length=2, choices=LeadConstant.LEAD_STATUS,
                              default=LeadConstant.OPEN, db_index=True)
    #Cannot use member because entity should always exist
    entity = models.ForeignKey(Entity, related_name='leads')
    employee = models.ForeignKey(Employee, related_name='leads')

    tasks = GenericRelation(Task, content_type_field='contact_ct', object_id_field='contact_id', related_query_name='lead')
    events = GenericRelation(Event, content_type_field='contact_ct', object_id_field='contact_id')
    notes = GenericRelation(Note)

    timeline = GenericRelation(Timeline)

    objects = LeadManager()

    def __unicode__(self):
        return str(self.first_name) + ' ' + str(self.entity) + ' ' + str(self.employee)

    def active_tasks(self):
        return self.tasks.filter(is_deleted=False)

    def active_events(self):
        return self.events.filter(is_deleted=False)

    def active_notes(self):
        return self.notes.filter(is_deleted=False)

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