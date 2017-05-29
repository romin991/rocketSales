from __future__ import absolute_import, unicode_literals
from celery import shared_task
from reports.utils import *
from reports.constants import *

@shared_task
def async_generate_report(pk):
    try:
        generate_report(pk)
    except Exception as exc:
        report = Report.objects.get(pk=pk)
        report.status = ReportConstant.ERROR
        report.save()
        return