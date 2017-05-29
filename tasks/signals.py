from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import *
from algolias.utils import *
from timelines.utils import *
from tasks.utils import *
from algolias.celery_tasks import *

@receiver(post_save, sender=Task, dispatch_uid='task.tasks')
def task_post_save(sender, instance, created, **kwargs):
    task = instance
    action = task
    contact = task.contact_object
    employee = task.employee

    verb = create_task_verb(created, task.status)

    create_timeline(task.contact_object, contact, verb, action, employee)
    create_timeline(task.company, contact, verb, action, employee)

    if task.deal:
        create_timeline(task.deal, contact, verb, action, employee)

    async_register_algolia_update_signal.delay(instance.pk, instance._meta.model_name)
