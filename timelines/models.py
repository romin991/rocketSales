from __future__ import unicode_literals
from bases.models import *
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from timelines.utils import *


class TimelineManager(models.Manager):
    def create_timeline(self, content_object, **extra_fields):
        timeline = self.model(content_object=content_object, **extra_fields)
        timeline.content = {'timeline':[]}
        timeline.save()
        return timeline

# Create your models here.
class Timeline(BaseModel):
    content = JSONField(blank=False, default=dict)
    limit = models.Q(app_label='leads', model='lead') | models.Q(app_label='companies', model='company')\
        | models.Q(app_label='customers', model='customer')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = TimelineManager()

    def __unicode__(self):
        return str(self.content_object)

    def add_timeline_content(self, contact, verb, action, employee):
        timeline_dict = build_timeline_dict(contact, verb, action, employee)
        updated_content = self.content['timeline']
        updated_content.insert(0, timeline_dict)
        self.content['timeline'] = updated_content
        self.save()
        return self

    class Meta:
        unique_together = ('content_type', 'object_id')