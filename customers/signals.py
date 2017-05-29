from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from customers.models import *
from timelines.models import *
from algolias.celery_tasks import *

@receiver(post_save, sender=Customer, dispatch_uid='customer.customers')
def customer_post_save(sender, instance, created, **kwargs):
    if created:
        Timeline.objects.create_timeline(instance)

    async_register_algolia_update_signal.delay(instance.pk, instance._meta.model_name)