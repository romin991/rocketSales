from __future__ import absolute_import, unicode_literals
from celery import shared_task
from algolias.utils import *

@shared_task(bind=True, max_retries=3, soft_time_limit=30)
def async_register_algolia_update_signal(self, pk, model_name):
    try:
        ct = ContentType.objects.get(model=model_name)
        current_class = ct.model_class()
        instance = current_class.objects.get(pk=pk)
        register_algolia_update_signal(instance)
    except Exception as exc:
        self.retry(exc=exc)