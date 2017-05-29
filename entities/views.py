from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from bases.services import *
from entities.models import *
from entities.serializers import *
from rest_framework.decorators import detail_route
from entities.utils import *
#implement update & retrieve
class EntityViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(EntityViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def retrieve(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        entity = get_object_or_404(queryset)
        entity_serializer = EntitySerializer(entity)

        return Response(entity_serializer.data)

    def update(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        entity = get_object_or_404(queryset)
        entity_serializer = EntitySerializer(entity, data=request.data, partial=True)

        if entity_serializer.is_valid():
            entity_serializer.save()
            return Response(entity_serializer.data)
        return Response(entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'])
    def summary(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        summary = get_summary(entity_id)
        return Response(summary)

    def get_queryset(self, entity_id):
        queryset = Entity.objects.filter(id=entity_id)
        return queryset