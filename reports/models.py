from __future__ import unicode_literals

from django.db import models
from bases.models import *
from entities.models import *
from employees.models import *
from reports.constants import *
from django.contrib.postgres.fields import JSONField
# Create your models here.

class ReportManager(models.Manager):

    def create_report(self, type, employee, start_time, end_time, **extra_fields):
        report = self.model(type=type, employee=employee, start_time=start_time, end_time=end_time, **extra_fields)

        report.save()

        return report

class Report(BaseModel):
    type = models.CharField(max_length=2, choices=ReportConstant.REPORT_TYPE)
    employee = models.ForeignKey(Employee, related_name='reports', blank=True, null=True) # default to all
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    status = models.CharField(max_length=2, choices=ReportConstant.REPORT_STATUS, default=ReportConstant.QUEUE)
    url = models.TextField(blank=True)
    meta = JSONField(blank=False, default=dict)
    requester = models.ForeignKey(Employee, related_name='requested_reports')
    entity = models.ForeignKey(Entity, related_name='reports')

    objects = ReportManager()

    def get_employee_name(self, **kwargs):
        if self.employee:
            return self.employee.user.first_name
        else:
            return 'All Employee'

    def __unicode__(self):
        return str(self.type) + ' ' + str(self.get_employee_name()) + ' ' +\
               str(self.start_date) + ' ' + str(self.end_date)

