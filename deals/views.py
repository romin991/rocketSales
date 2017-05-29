from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from bases.services import *
from rest_framework import viewsets
from deals.models import *
from deals.serializers import *
from rest_framework import filters
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route, list_route
from django.db import transaction
from bases.views import *
from deals.utils import *

# Create your views here.
class DealViewSet(viewsets.GenericViewSet, CommonCrudMixin, CommonExtensionMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('employee', 'company', 'customer', 'status',)

    def __init__(self, *args, **kwargs):
        super(DealViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, DealFullSerializer)

    def list(self, request):
        return self.list_helper(request, DealSerializer)

    #Already limited to a particular entity_id
    def retrieve(self, request, pk=None):
        return self.retrieve_helper(request, pk, DealFullSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, DealFullSerializer)

    def destroy(self, request, pk=None):
        return self.destroy_helper(request, pk)

    @transaction.atomic
    def perform_destroy(self, deal):
        deal.tasks.update(is_deleted=True)
        deal.events.update(is_deleted=True)
        deal.notes.update(is_deleted=True)
        deal.is_deleted = True
        deal.save()
        return

    @detail_route(methods=['get'])
    def tasks(self, request, pk=None):
        return self.task_helper(request, pk)

    @detail_route(methods=['get'])
    def events(self, request, pk=None):
        return self.event_helper(request, pk)

    @detail_route(methods=['get'])
    def timelines(self, request, pk=None):
        return self.timeline_helper(request, pk)

    @detail_route(methods=['get'])
    def notes(self, request, pk=None):
        return self.note_helper(request, pk)

    @list_route(methods=['get'])
    def summary(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        summary = get_summary(entity_id)
        return Response(summary)

    def get_queryset(self, entity_id):
        queryset = Deal.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset

class DealMobileViewSet(viewsets.GenericViewSet, CommonMobileCrudMixin):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(DealMobileViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, DealMobileCreateSerializer)

    def list(self, request):
        return self.sync_helper(request, DealMobileSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, DealMobileUpdateSerializer)

    #Query set return all include the one that is_deleted=True
    def get_queryset(self, entity_id):
        queryset = Deal.objects.filter(entity=entity_id)
        return queryset