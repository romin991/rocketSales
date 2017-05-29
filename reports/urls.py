from django.conf.urls import url, include
from reports.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'reports', ReportViewSet, base_name='report')

urlpatterns = [
    url(r'', include(router.urls)),
]
