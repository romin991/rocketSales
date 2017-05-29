from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from bases.services import *
from rest_framework import viewsets
from customers.models import *
from customers.serializers import *
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from customers.importers import *
from events.constants import *
from bases.views import *

# Create your views here.
class CustomerImport(APIView, CommonImportMixin):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def __init__(self, *args, **kwargs):
        super(CustomerImport, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    #Atomic transaction on helper method
    def post(self, request, format=None):
        return self.import_helper(request, CustomerModelImporter, CustomerSerializer)

class CustomerViewSet(viewsets.GenericViewSet, CommonCrudMixin, CustomerExtensionMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('employee',)

    def __init__(self, *args, **kwargs):
        super(CustomerViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, CustomerFullSerializer)

    def list(self, request):
        return self.list_helper(request, CustomerSerializer)

    #Already limited to a particular entity_id
    def retrieve(self, request, pk=None):
        return self.retrieve_helper(request, pk, CustomerFullSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, CustomerFullSerializer)

    def destroy(self, request, pk=None):
        return self.destroy_helper(request, pk)

    @transaction.atomic
    def perform_destroy(self, customer):
        customer.tasks.update(is_deleted=True)
        customer.notes.update(is_deleted=True)
        customer.deals.update(is_deleted=True)
        customer.is_deleted = True
        customer.save()
        return

#Refactor this, put together Lead, Customer, Account
#TODO If invalid filter return 0
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
        queryset = Customer.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset


class CustomerMobileViewSet(viewsets.GenericViewSet, CommonMobileCrudMixin):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(CustomerMobileViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, CustomerMobileCreateSerializer)

    def list(self, request):
        return self.sync_helper(request, CustomerMobileSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, CustomerMobileUpdateSerializer)

    #Query set return all include the one that is_deleted=True
    def get_queryset(self, entity_id):
        queryset = Customer.objects.filter(entity=entity_id)
        return queryset