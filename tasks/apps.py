from __future__ import unicode_literals

from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'tasks'
    verbose_name = 'Tasks Application'

    def ready(self):
        import tasks.signals