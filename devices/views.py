from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from bases.services import *
from django.db import transaction
from rest_framework import viewsets
from bases.views import *
from devices.serializers import *
from devices.permissions import *

class DeviceViewSet(viewsets.GenericViewSet, CommonCreateMixin, CommonDestroyMixin):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def __init__(self, *args, **kwargs):
        super(DeviceViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        return self.create_helper(request, DeviceSerializer)

    def destroy(self, request, pk=None):
        return self.destroy_helper(request, pk)

    @transaction.atomic
    def perform_destroy(self, device):
        device.is_deleted = True
        device.save()
        return

    def get_queryset(self, entity_id):
        queryset = Device.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset