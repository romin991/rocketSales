from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from bases.services import *
from rest_framework import viewsets
from events.serializers import *
from rest_framework import filters
from django.shortcuts import get_object_or_404
from django.db import transaction
from events.filters import *
from bases.views import *
from rest_framework.decorators import detail_route

class EventViewSet(viewsets.GenericViewSet, CommonCrudMixin, ActionExtensionMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EventFilter

    def __init__(self, *args, **kwargs):
        super(EventViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, EventFullSerializer)

    def list(self, request):
        return self.list_helper(request, EventSerializer)

    def retrieve(self, request, pk=None):
        return self.retrieve_helper(request, pk, EventFullSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, EventFullSerializer)

    def destroy(self, request, pk=None):
        return self.destroy_helper(request, pk)

    @detail_route(methods=['get'])
    def companies(self, request, pk=None):
        return self.company_helper(request, pk)

    @detail_route(methods=['get'])
    def contacts(self, request, pk=None):
        return self.contact_helper(request, pk)

    @detail_route(methods=['get'])
    def notes(self, request, pk=None):
        return self.note_helper(request, pk)

    @transaction.atomic
    def perform_destroy(self, event):
        event.notes.update(is_deleted=True)
        event.is_deleted = True
        event.save()
        return

    def get_queryset(self, entity_id):
        queryset = Event.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset

class EventMobileViewSet(viewsets.GenericViewSet, CommonMobileCrudMixin):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(EventMobileViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, EventMobileCreateSerializer)

    def list(self, request):
        return self.sync_helper(request, EventMobileSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, EventMobileUpdateSerializer)

    #Query set return all include the one that is_deleted=True
    def get_queryset(self, entity_id):
        queryset = Event.objects.filter(entity=entity_id)
        return queryset