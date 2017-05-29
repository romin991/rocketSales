from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from bases.models import *
from entities.models import *
from deals.constants import *
from tasks.constants import *
from timelines.mixins import *
from employees.constants import *
from accounts.models import *
# Create your models here.
class EmployeeManager(models.Manager):

    def create_employee(self, user, **extra_fields):
        employee = self.model(user=user, **extra_fields)

        employee.save()
        return employee

class MembershipManager(models.Manager):

    def create_membership(self, employee, entity, **extra_fields):
        membership = self.model(employee=employee, entity=entity, **extra_fields)

        membership.save()
        return membership


class Employee(models.Model, TimelineMixin):
    ADMIN = 'A'
    WORKER = 'W'

    EMPLOYEE_ROLE = (
        (ADMIN, 'Admin'),
        (WORKER, 'Worker'),
    )

    user = models.OneToOneField(Account, primary_key=True)
    phone = models.CharField(blank=True, max_length=40)
    prof_pic = models.TextField(blank=True)
    members = models.ManyToManyField(Entity, through='Membership')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()

    def __unicode__(self):
        return str(self.user.email)

    def active_leads(self):
        return self.leads.filter(is_deleted=False)

    def active_customers(self):
        return self.customers.filter(is_deleted=False)

    def active_companies(self):
        return self.companies.filter(is_deleted=False)

    def active_deals(self):
        return self.deals.filter(is_deleted=False)

    def active_tasks(self):
        return self.tasks.filter(is_deleted=False)

    def active_events(self):
        return self.events.filter(is_deleted=False)

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
        return str(self.user.first_name)

#Membership is just use during authentication, and choosing company
class Membership(BaseModel):
    employee = models.ForeignKey(Employee)
    entity = models.ForeignKey(Entity, related_name='members')
    role = models.CharField(max_length=2, choices=EmployeeConstant.ROLE_STATUS,
                              default=EmployeeConstant.EMPLOYEE)
    objects = MembershipManager()

    def __unicode__(self):
        return str(self.entity) + ' ' + str(self.employee)