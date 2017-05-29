from __future__ import unicode_literals

from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'events'
    verbose_name = 'Events Application'

    def ready(self):
        import events.signals
