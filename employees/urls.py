from django.conf.urls import url, include
from employees.views import *
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from employees.views import *
router = routers.SimpleRouter()
router.register(r'employees', EmployeeViewSet, base_name='employee')
router.register(r'memberships', MembershipViewSet, base_name='membership')
router.register(r'membership-mobiles', MembershipMobileViewSet, base_name='membership-mobile')

urlpatterns = [
    url(r'^register/$', RegisterUser.as_view()),
    url(r'^register/add/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activation_confirm, name='activation_confirm'),
    url(r'^register/add/complete/$', activation_complete, name='activation_complete'),
    url(r'^register/reset/$', Reset.as_view()),
    url(r'^register/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', reset_confirm, name='reset_confirm'),
    url(r'^register/reset/complete/$', reset_complete, name='reset_complete'),
    url(r'^login/$', obtain_jwt_token),
    url(r'', include(router.urls)),
]
