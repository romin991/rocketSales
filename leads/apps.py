from __future__ import unicode_literals

from django.apps import AppConfig


class LeadsConfig(AppConfig):
    name = 'leads'
    verbose_name = 'Leads Application'

    def ready(self):
        import leads.signals
