from __future__ import unicode_literals

from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    name = 'companies'
    verbose_name = 'Companies Application'

    def ready(self):
        import companies.signals
