from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from bases.services import *
from rest_framework import viewsets
from notes.models import *
from notes.serializers import *
from rest_framework import filters
from rest_framework import generics
from django.shortcuts import get_object_or_404
from bases.views import *

# Create your views here.
class NoteViewSet(viewsets.GenericViewSet, CommonCreateMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('employee',)

    def __init__(self, *args, **kwargs):
        super(NoteViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, NoteSerializer)

    def destroy(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        note = get_object_or_404(queryset, pk=pk, employee=request.user.id)
        self.perform_destroy(note)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, note):
        note.is_deleted = True
        note.save()
        return note

    def get_queryset(self, entity_id):
        queryset = Note.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset

class NoteMobileViewSet(viewsets.GenericViewSet, CommonMobileSyncMixin, CommonMobileCreateMixin):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(NoteMobileViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, NoteMobileCreateSerializer)

    def list(self, request):
        return self.sync_helper(request, NoteMobileSerializer)

    #Query set return all include the one that is_deleted=True
    def get_queryset(self, entity_id):
        queryset = Note.objects.filter(entity=entity_id)
        return queryset