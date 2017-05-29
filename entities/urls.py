from django.conf.urls import url, include
from entities.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'entities', EntityViewSet, base_name='entity')

urlpatterns = [
    url(r'', include(router.urls)),
]
