from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import *
from algolias.utils import *
from timelines.utils import *
from events.utils import *
from algolias.celery_tasks import *

@receiver(post_save, sender=Event, dispatch_uid='event.events')
def event_post_save(sender, instance, created, **kwargs):
    event = instance
    action = event
    contact = event.contact_object
    employee = event.employee

    verb = create_event_verb(created)

    create_timeline(event.contact_object, contact, verb, action, employee)
    create_timeline(event.company, contact, verb, action, employee)

    if event.deal:
        create_timeline(event.deal, contact, verb, action, employee)

    async_register_algolia_update_signal.delay(instance.pk, instance._meta.model_name)

