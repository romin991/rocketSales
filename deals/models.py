from __future__ import unicode_literals

from django.db import models
from entities.models import *
from employees.models import *
from companies.models import *
from customers.models import *
from django.contrib.contenttypes.fields import GenericRelation
from tasks.models import *
from notes.models import *
from deals.constants import *
from timelines.mixins import *
# Create your models here.

class DealManager(models.Manager):

    def create_deal(self, name, entity, employee, customer, **extra_fields):
        deal = self.model(name=name, entity=entity, employee=employee, customer=customer, **extra_fields)

        deal.save()

        return deal

class Deal(BaseCoreModel, TimelineMixin):

    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True)

    expected_revenue = models.BigIntegerField(blank=True, default=0)
    expected_closing_date = models.DateField(blank=True, null=True)

    closing_revenue = models.BigIntegerField(blank=True, default=0)
    lost_note = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=2, choices=DealConstant.DEAL_STATUS,
                              default=DealConstant.OPEN, db_index=True)

    #Cannot use member because entity should always exist
    entity = models.ForeignKey(Entity, related_name='deals')
    employee = models.ForeignKey(Employee, related_name='deals')
    company = models.ForeignKey(Company, null=True, blank=True, related_name='deals')
    customer = models.ForeignKey(Customer, related_name='deals')

    notes = GenericRelation(Note)

    timeline = GenericRelation(Timeline)

    objects = DealManager()

    def __unicode__(self):
        return str(self.name) + ' ' + str(self.entity) + ' ' + str(self.employee) +\
            ' ' + str(self.company) + ' ' + str(self.customer)

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
        return str(self.name)

    def get_expected_closing_date(self):
        if self.expected_closing_date == None:
            return int(time.mktime(datetime(2030, 1, 1, 0, 0).timetuple()))
        return int(time.mktime(self.expected_closing_date.timetuple()))

    def get_epoch_created_at(self):
        return int(time.mktime(self.created_at.timetuple()))

    class Meta:
        ordering = ['expected_closing_date', '-created_at']