from django.conf.urls import url, include
from customers.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'customers', CustomerViewSet, base_name='customer')
router.register(r'customer-mobiles', CustomerMobileViewSet, base_name='customer-mobile')

urlpatterns = [
    url(r'^customers-import/$', CustomerImport.as_view()),
    url(r'', include(router.urls)),
]
