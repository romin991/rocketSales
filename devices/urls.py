from django.conf.urls import url, include
from devices.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'devices', DeviceViewSet, base_name='device')

urlpatterns = [
    url(r'', include(router.urls)),
]
