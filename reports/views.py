from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from bases.services import *
from django.db import transaction
from rest_framework import viewsets
from bases.views import *
from reports.serializers import *
from reports.celery_tasks import *

class ReportViewSet(viewsets.GenericViewSet, CommonListMixin, CommonRetrieveMixin):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(ReportViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def create(self, request):
        entity_id = self.entity_service.get_entity_id(request)
        data = request.data
        data['entity'] = entity_id
        data['requester'] = request.user.id
        serializer = ReportFullSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            async_generate_report.delay(serializer.data.get('id'))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id).order_by('-created_at')
        filtered_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = ReportSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        #Never happen when we use pagenumber pagination
        return Response()

    def retrieve(self, request, pk=None):
        return self.retrieve_helper(request, pk, ReportFullSerializer)

    def get_queryset(self, entity_id):
        queryset = Report.objects.filter(entity=entity_id).filter(is_deleted=False)
        return queryset