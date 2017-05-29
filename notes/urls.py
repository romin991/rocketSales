from django.conf.urls import url, include
from notes.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'notes', NoteViewSet, base_name='note')
router.register(r'note-mobiles', NoteMobileViewSet, base_name='note-mobile')

urlpatterns = [
    url(r'', include(router.urls)),
]
