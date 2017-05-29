from django.conf.urls import url, include
from leads.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'leads', LeadViewSet, base_name='lead')
router.register(r'lead-mobiles', LeadMobileViewSet, base_name='lead-mobile')

urlpatterns = [
    url(r'^leads-import/$', LeadImport.as_view()),
    url(r'', include(router.urls)),
]
