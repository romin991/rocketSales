from django.conf.urls import url, include
from bases.views import *

urlpatterns = [
    url(r'^sync/$', Sync.as_view()),
    url(r'^sendMessage/$', SendMessage.as_view()),
]
