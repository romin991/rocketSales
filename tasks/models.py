from __future__ import unicode_literals

from django.db import models
from entities.models import *
from employees.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from notes.models import *
from tasks.constants import *
from timelines.mixins import *
from datetime import datetime
import time

class TaskManager(models.Manager):

    def create_task(self, subject, entity, employee, contact_object, **extra_fields):
        task = self.model(subject=subject, entity=entity, employee=employee,
                          contact_object=contact_object, **extra_fields)

        task.save()

        return task

# Create your models here.
class Task(BaseCoreModel, TimelineMixin):
    subject = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=2, choices=TaskConstant.TASK_PRIORITY,
                                default=TaskConstant.MEDIUM, db_index=True)
    due_date = models.DateField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=2, choices=TaskConstant.TASK_STATUS,
                              default=TaskConstant.OPEN, db_index=True)
    #Cannot use member because entity should always exist
    entity = models.ForeignKey(Entity, related_name='tasks')
    employee = models.ForeignKey(Employee, related_name='tasks')

    #lead does not have company
    company = models.ForeignKey('companies.Company', null=True, blank=True, related_name='tasks')

    contact_limit = models.Q(app_label='leads', model='lead') | models.Q(app_label='customers', model='customer')
    contact_ct = models.ForeignKey(ContentType, limit_choices_to=contact_limit)
    contact_id = models.UUIDField()
    contact_object = GenericForeignKey('contact_ct', 'contact_id')

    deal = models.ForeignKey('deals.Deal', null=True, blank=True, related_name="tasks")

    notes = GenericRelation(Note)

    objects = TaskManager()

    def __unicode__(self):
        return str(self.subject) + ' ' + str(self.entity) + ' ' + str(self.employee) +\
            ' ' + str(self.contact_object)

    def active_notes(self):
        return self.notes.filter(is_deleted=False)

    def get_timeline_title(self):
        return str(self.subject)

    def get_epoch_due_date(self):
        if self.due_date == None:
            return int(time.mktime(datetime(2030, 1, 1, 0, 0).timetuple()))
        return int(time.mktime(self.due_date.timetuple()))

    def get_epoch_created_at(self):
        return int(time.mktime(self.created_at.timetuple()))

    def get_company_name(self):
        company_name = ''
        if self.contact_ct == ContentType.objects.get(model="lead"):
            company_name = self.contact_object.company_name
        elif self.contact_ct == ContentType.objects.get(model="customer"):
            if self.company:
                company_name = self.company.name
        return company_name

    class Meta:
        ordering = ['due_date', '-created_at']