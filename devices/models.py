from __future__ import unicode_literals

from django.db import models
from bases.models import *
from entities.models import *
from employees.models import *
# Create your models here.

class DeviceManager(models.Manager):

    def create_device(self, reg_id, entity, employee, **extra_fields):
        device = self.model(reg_id=reg_id, entity=entity, employee=employee, **extra_fields)

        device.save()
        return device

class Device(BaseModel):
    reg_id = models.CharField(max_length=255)
    entity = models.ForeignKey(Entity, related_name='devices')
    employee = models.ForeignKey(Employee, related_name='devices')

    objects = DeviceManager()

    def __unicode__(self):
        return str(self.reg_id) + ' ' + str(self.entity) + ' ' + str(self.employee)
