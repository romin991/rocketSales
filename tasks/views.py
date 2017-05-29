from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from bases.services import *
from rest_framework import viewsets
from tasks.models import *
from tasks.serializers import *
from rest_framework import filters
from rest_framework import generics
from django.shortcuts import get_object_or_404
from leads.models import *
from companies.models import *
from customers.models import *
from deals.models import *
from django.db import transaction
from bases.views import *
from rest_framework.decorators import detail_route

# Create your views here.
class TaskViewSet(viewsets.GenericViewSet, CommonCrudMixin, ActionExtensionMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('employee', 'contact_ct', 'contact_id', 'status', 'company', 'priority',)

    def __init__(self, *args, **kwargs):
        super(TaskViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, TaskFullSerializer)

    def list(self, request):
        return self.list_helper(request, TaskSerializer)

    #Already limited to a particular entity_id
    def retrieve(self, request, pk=None):
        return self.retrieve_helper(request, pk, TaskFullSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, TaskFullSerializer)

    def destroy(self, request, pk=None):
        return self.destroy_helper(request, pk)

    @transaction.atomic
    def perform_destroy(self, task):
        task.notes.update(is_deleted=True)
        task.is_deleted = True
        task.save()
        return

    @detail_route(methods=['get'])
    def companies(self, request, pk=None):
        return self.company_helper(request, pk)

    @detail_route(methods=['get'])
    def contacts(self, request, pk=None):
        return self.contact_helper(request, pk)

    @detail_route(methods=['get'])
    def notes(self, request, pk=None):
        return self.note_helper(request, pk)

    def get_queryset(self, entity_id):
        queryset = Task.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset

class TaskMobileViewSet(viewsets.GenericViewSet, CommonMobileCrudMixin):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(TaskMobileViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, TaskMobileCreateSerializer)

    def list(self, request):
        return self.sync_helper(request, TaskMobileSerializer)

    def update(self, request, pk=None):
        return self.update_helper(request, pk, TaskMobileUpdateSerializer)

    #Query set return all include the one that is_deleted=True
    def get_queryset(self, entity_id):
        queryset = Task.objects.filter(entity=entity_id)
        return queryset