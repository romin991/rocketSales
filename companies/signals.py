from django.db.models.signals import post_save
from django.dispatch import receiver
from companies.models import *
from timelines.models import *
from algolias.celery_tasks import *

@receiver(post_save, sender=Company, dispatch_uid='company.companies')
def company_post_save(sender, instance, created, **kwargs):
    if created:
        Timeline.objects.create_timeline(instance)

    async_register_algolia_update_signal.delay(instance.pk, instance._meta.model_name)