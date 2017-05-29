from django.db.models.signals import post_save
from django.dispatch import receiver
from deals.models import *
from timelines.utils import *
from deals.utils import *
from algolias.utils import *
from algolias.celery_tasks import *

@receiver(post_save, sender=Deal, dispatch_uid='deal.deals')
def deal_post_save(sender, instance, created, **kwargs):

    if created:
        Timeline.objects.create_timeline(instance)

    deal = instance
    action = deal
    contact = deal.customer
    employee = deal.employee
    verb = create_deal_verb(created, deal.status)

    create_timeline(deal.customer, contact, verb, action, employee)
    create_timeline(deal.company, contact, verb, action, employee)

    async_register_algolia_update_signal.delay(instance.pk, instance._meta.model_name)