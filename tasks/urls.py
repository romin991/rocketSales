from django.conf.urls import url, include
from tasks.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tasks', TaskViewSet, base_name='task')
router.register(r'task-mobiles', TaskMobileViewSet, base_name='task-mobile')

urlpatterns = [
    url(r'', include(router.urls)),
]
