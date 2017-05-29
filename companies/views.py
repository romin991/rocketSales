from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from bases.services import *
from rest_framework import viewsets
from companies.models import *
from companies.serializers import *
from rest_framework import filters
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from companies.importers import *
from events.constants import *
from bases.views import *
# Create your views here.
class CompanyImport(APIView, CommonImportMixin):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def __init__(self, *args, **kwargs):
        super(CompanyImport, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    #Atomic transaction on helper method
    def post(self, request, format=None):
        return self.import_helper(request, CompanyModelImporter, CompanySerializer)

class CompanyViewSet(viewsets.GenericViewSet, CommonCrudMixin, AccountExtensionMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('employee',)

    def __init__(self, *args, **kwargs):
        super(CompanyViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, CompanyFullSerializer)

    def list(self, request):
        return self.list_helper(request, CompanySerializer)

    #Already limited to a particular entity_id
    def retrieve(self, request, pk=None):
        return self.retrieve_helper(request, pk, CompanyFullSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, CompanyFullSerializer)

    def destroy(self, request, pk=None):
        return self.destroy_helper(request, pk)

    @transaction.atomic
    def perform_destroy(self, company):
        company.tasks.update(is_deleted=True)
        company.notes.update(is_deleted=True)
        company.deals.update(is_deleted=True)
        company.customers.update(is_deleted=True)
        company.is_deleted = True
        company.save()
        return

    @detail_route(methods=['get'])
    def tasks(self, request, pk=None):
        return self.task_helper(request, pk)

    @detail_route(methods=['get'])
    def events(self, request, pk=None):
        return self.event_helper(request, pk)

    @detail_route(methods=['get'])
    def deals(self, request, pk=None):
        return self.deal_helper(request, pk)

    @detail_route(methods=['get'])
    def timelines(self, request, pk=None):
        return self.timeline_helper(request, pk)

    @detail_route(methods=['get'])
    def notes(self, request, pk=None):
        return self.note_helper(request, pk)

    def get_queryset(self, entity_id):
        queryset = Company.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset

class CompanyMobileViewSet(viewsets.GenericViewSet, CommonMobileCrudMixin):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(CompanyMobileViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, CompanyMobileCreateSerializer)

    def list(self, request):
        return self.sync_helper(request, CompanyMobileSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, CompanyMobileUpdateSerializer)

    #Query set return all include the one that is_deleted=True
    def get_queryset(self, entity_id):
        queryset = Company.objects.filter(entity=entity_id)
        return queryset