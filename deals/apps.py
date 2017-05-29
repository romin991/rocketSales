from __future__ import unicode_literals

from django.apps import AppConfig


class DealsConfig(AppConfig):
    name = 'deals'
    verbose_name = 'Deals Application'

    def ready(self):
        import deals.signals