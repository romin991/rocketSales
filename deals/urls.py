from django.conf.urls import url, include
from deals.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'deals', DealViewSet, base_name='deal')
router.register(r'deal-mobiles', DealMobileViewSet, base_name='deal-mobile')

urlpatterns = [
    url(r'', include(router.urls)),
]
