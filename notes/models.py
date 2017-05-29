from __future__ import unicode_literals

from django.db import models
from bases.models import *
from entities.models import *
from employees.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class NoteManager(models.Manager):

    def create_note(self, note, entity, employee, content_object, **extra_fields):
        note = self.model(note=note, entity=entity, employee=employee,
                          content_object=content_object, **extra_fields)

        note.save()

        return note

class Note(BaseCoreModel):
    note = models.TextField(blank=False, null=False)

    #Cannot use member because entity should always exist
    entity = models.ForeignKey(Entity, related_name='notes')
    employee = models.ForeignKey(Employee, related_name='notes')

    limit = models.Q(app_label='leads', model='lead') | models.Q(app_label='companies', model='company')\
            | models.Q(app_label='customers', model='customer') | models.Q(app_label='deals', model='deal')\
            | models.Q(app_label='tasks', model='task')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = NoteManager()

    def __unicode__(self):
        return str(self.employee) + ' ' + str(self.entity) + ' ' + str(self.note) +\
            ' ' + str(self.content_object)

    class Meta:
        ordering = ['-created_at']
