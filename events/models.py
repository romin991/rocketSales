from __future__ import unicode_literals

from django.db import models
from bases.models import *
from entities.models import *
from employees.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from notes.models import *
import time

class EventManager(models.Manager):

    def create_event(self, subject, entity, employee, contact_object, start_time, duration, **extra_fields):
        event = self.model(subject=subject, entity=entity, employee=employee,
                           contact_object=contact_object, start_time=start_time,
                           duration=duration, **extra_fields)

        event.save()
        return event

# Create your models here.
class Event(BaseCoreModel, TimelineMixin):
    subject = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True)

    street = models.TextField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    state = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=255)
    pos_code = models.CharField(blank=True, max_length=255)

    start_time = models.DateTimeField(blank=False, null=False, db_index=True)
    duration = models.IntegerField(blank=False, null=False)

    entity = models.ForeignKey(Entity, related_name='events')
    employee = models.ForeignKey(Employee, related_name='events')

    #lead does not have company
    company = models.ForeignKey('companies.Company', null=True, blank=True, related_name='events')

    contact_limit = models.Q(app_label='leads', model='lead') | models.Q(app_label='customers', model='customer')
    contact_ct = models.ForeignKey(ContentType, limit_choices_to=contact_limit)
    contact_id = models.UUIDField()
    contact_object = GenericForeignKey('contact_ct', 'contact_id')

    deal = models.ForeignKey('deals.Deal', null=True, blank=True, related_name="events")

    notes = GenericRelation(Note)

    objects = EventManager()

    def __unicode__(self):
        return str(self.subject) + ' ' + str(self.entity) + ' ' + str(self.employee) +\
            ' ' + str(self.contact_object)

    def active_notes(self):
        return self.notes.filter(is_deleted=False)

    def get_timeline_title(self):
        return str(self.subject)

    def get_epoch_start_time(self):
        return int(time.mktime(self.start_time.timetuple()))

    def get_company_name(self):
        company_name = ''
        if self.contact_ct == ContentType.objects.get(model="lead"):
            company_name = self.contact_object.company_name
        elif self.contact_ct == ContentType.objects.get(model="customer"):
            if self.company:
                company_name = self.company.name
        return company_name

    class Meta:
        ordering = ['start_time', '-created_at']
