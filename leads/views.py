from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from bases.services import *
from rest_framework import viewsets
from leads.models import *
from leads.serializers import *
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from customers.serializers import *
from companies.serializers import *
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from leads.importers import *
from tasks.serializers import *
from events.serializers import *
from events.constants import *
from bases.views import *
from leads.utils import *

# Create your views here.
class LeadImport(APIView, CommonImportMixin):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def __init__(self, *args, **kwargs):
        super(LeadImport, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    #Atomic transaction on helper method
    def post(self, request, format=None):
        return self.import_helper(request, LeadModelImporter, LeadSerializer)

class LeadViewSet(viewsets.GenericViewSet, CommonCrudMixin, CommonExtensionMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('employee', 'status', 'lead_source', )

    def __init__(self, *args, **kwargs):
        super(LeadViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, LeadFullSerializer)

    def list(self, request):
        return self.list_helper(request, LeadSerializer)

    def retrieve(self, request, pk=None):
        return self.retrieve_helper(request, pk, LeadFullSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, LeadFullSerializer)

    def destroy(self, request, pk=None):
        return self.destroy_helper(request, pk)

    @transaction.atomic
    def perform_destroy(self, lead):
        lead.tasks.update(is_deleted=True)
        lead.notes.update(is_deleted=True)
        lead.is_deleted = True
        lead.save()
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

    @detail_route(methods=['post'])
    @transaction.atomic
    def convert(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        lead = get_object_or_404(queryset, pk=pk)

        if lead.status == LeadConstant.CONVERTED:
            return Response()

        lead.status = LeadConstant.CONVERTED
        lead.save()

        customer_lead_data = LeadFullSerializer(lead).data
        customer_lead_data['lead_origin'] = lead.id

        company_name = customer_lead_data.get('company_name', '')

        if company_name != '':
            company_data = dict()
            company_data['name'] = company_name
            company_data['entity'] = customer_lead_data['entity']
            company_data['employee'] = customer_lead_data['employee']

            company_full_serializer = CompanyFullSerializer(data=company_data)
            if not company_full_serializer.is_valid():
                return Response(company_full_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            company = company_full_serializer.save()
            customer_lead_data['company'] = company.id

        customer_full_serializer = CustomerFullSerializer(data=customer_lead_data)

        if not customer_full_serializer.is_valid():
            return Response(customer_full_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        customer = customer_full_serializer.save()

        result = LeadFullSerializer(lead).data

        #Hacky to bypass transaction commit
        result['converted_customer'] = customer.id
        result['converted_customer_first_name'] = customer.first_name
        result['converted_customer_last_name'] = customer.last_name
        return Response(result)

    @list_route(methods=['get'])
    def summary(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        summary = get_summary(entity_id)
        return Response(summary)

    def get_queryset(self, entity_id):
        queryset = Lead.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset

class LeadMobileViewSet(viewsets.GenericViewSet, CommonMobileCrudMixin):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(LeadMobileViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, LeadMobileCreateSerializer)

    def list(self, request):
        return self.sync_helper(request, LeadMobileSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, LeadMobileUpdateSerializer)

    #Query set return all include the one that is_deleted=True
    def get_queryset(self, entity_id):
        queryset = Lead.objects.filter(entity=entity_id)
        return queryset