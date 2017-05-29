from django.conf.urls import url, include
from companies.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'companies', CompanyViewSet, base_name='company')
router.register(r'company-mobiles', CompanyMobileViewSet, base_name='company-mobile')
urlpatterns = [
    url(r'^companies-import/$', CompanyImport.as_view()),
    url(r'', include(router.urls)),
]
