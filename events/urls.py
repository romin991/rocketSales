from django.conf.urls import url, include
from events.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'events', EventViewSet, base_name='event')
router.register(r'event-mobiles', EventMobileViewSet, base_name='event-mobile')
urlpatterns = [
    url(r'', include(router.urls)),
]
