from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from bases.services import *
from entities.models import *
from algolias.utils import *
from bases.utils import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from events.constants import *
from bases.serializers import *
from django.utils import timezone
from dateutil.parser import parse as parse_date

class Sync(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(Sync, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def get(self, request, format=None):
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        prof_pic = request.user.employee.prof_pic
        entity_id = self.entity_service.get_entity_id(request)
        entity = Entity.objects.get(id=entity_id)
        expired = entity.expired
        max_user = entity.max_user
        role = Membership.objects.filter(entity=entity_id).filter(employee=request.user.pk).first().role
        algolia_meta = get_algolilas_meta(entity_id)
        model_meta = get_model_meta()
        cloudinary_meta = get_cloudinary_meta()
        return Response({"entity_id": entity_id, "employee_id": request.user.pk, "first_name": first_name, "last_name": last_name,
                         "email": email, "prof_pic": prof_pic, "expired": expired, "max_user": max_user, "role": role, "algolia_meta": algolia_meta,
                         "model_meta": model_meta, "cloudinary_meta": cloudinary_meta})


class SendMessage(APIView):
    def post(self, request, format=None):
        data = request.data
        serializer = SendMessageSerializer(data=data)
        if serializer.is_valid():
            EmailThread(serializer.data['name'], serializer.data['email'], serializer.data['phone'], serializer.data['message']).start()
            return Response({'status': 'Ok'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommonListMixin(object):

    def list_helper(self, request, serializer_class):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        filtered_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        #Never happen when we use pagenumber pagination
        return Response()

class CommonCreateMixin(object):

    def create_helper(self, request, serializer_class):
        entity_id = self.entity_service.get_entity_id(request)
        data = request.data
        data['entity'] = entity_id
        data['employee'] = data.get('employee') or request.user.id #Employee id is the same as user id
        data['global_last_changed'] = timezone.now()
        serializer = serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommonRetrieveMixin(object):

    def retrieve_helper(self, request, pk, serializer_class):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)
        serializer = serializer_class(object)

        return Response(serializer.data)

class CommonUpdateMixin(object):

    def update_helper(self, request, pk, serializer_class):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)
        data = request.data
        data['global_last_changed'] = timezone.now()
        serializer = serializer_class(object, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommonDestroyMixin(object):

    def destroy_helper(self,request, pk):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(object)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommonTaskMixin(object):

    def task_helper(self, request, pk):
        status = request.GET.get('status', '')
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)

        if not status in [s[0] for s in TaskConstant.TASK_STATUS]:
            return Response()

        task = object.active_tasks().filter(status=status)

        task_page = self.paginate_queryset(task)
        if task_page is not None:
            task_serializer = TaskSerializer(task_page, many=True)
            return self.get_paginated_response(task_serializer.data)

        #Never happen when we use pagenumber pagination
        return Response()

class CommonEventMixin(object):

    def event_helper(self, request, pk):
        status = request.GET.get('status', '')
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)
        if status == EventConstant.OPEN:
            event = object.active_open_events()
        elif status == EventConstant.CLOSED:
            event = object.active_closed_events()
        else:
            return Response()

        event_page= self.paginate_queryset(event)
        if event_page is not None:
            event_serializer = EventSerializer(event_page, many=True)
            return self.get_paginated_response(event_serializer.data)

        #Never happen when we use pagenumber pagination
        return Response()

class CommonDealMixin(object):

    def deal_helper(self, request, pk):
        status = request.GET.get('status', '')
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)

        if not status in [s[0] for s in DealConstant.DEAL_STATUS]:
            return Response()

        deal = object.active_deals().filter(status=status)

        deal_page = self.paginate_queryset(deal)
        if deal_page is not None:
            deal_serializer = DealSerializer(deal_page, many=True)
            return self.get_paginated_response(deal_serializer.data)

        #Never happen when we use pagenumber pagination
        return Response()

class CommonNoteMixin(object):

    def note_helper(self, request, pk):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)
        note_serializer = NoteSerializer(object.active_notes(), many=True)
        return Response(note_serializer.data)

class CommonCompanyMixin(object):

    def company_helper(self, request, pk):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)
        company_serializer = CompanySerializer(object.company)
        return Response(company_serializer.data)

class CommonContactMixin(object):

    def contact_helper(self, request, pk):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)
        contact = object.contact_object
        ct = 0
        if contact._meta.object_name == Lead._meta.object_name:
            serializer_class = LeadSerializer
            lead_object_name = Lead._meta.object_name.lower()
            ct = ContentType.objects.get(model=lead_object_name).id
        elif contact._meta.object_name == Customer._meta.object_name:
            serializer_class = CustomerSerializer
            customer_object_name = Customer._meta.object_name.lower()
            ct = ContentType.objects.get(model=customer_object_name).id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializer_class(contact)
        result = serializer.data
        result['ct'] = ct
        return Response(result)

class CommonTimelineMixin(object):

    def timeline_helper(self, request, pk):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)
        return Response(object.timeline.first().content['timeline'])

class CommonImportMixin(object):

    def import_helper(self, request, importer_class, serializer_class):
        entity_id = self.entity_service.get_entity_id(request)
        employee = request.user.employee
        entity = Entity.objects.get(id=entity_id)
        file_data = request.FILES['file']
        importer = importer_class(entity, employee)
        objects = importer.import_data(file_data)
        serializer = serializer_class(objects, many=True)

        return Response(serializer.data)

class CommonMobileSyncMixin(object):

    def sync_helper(self, request, serializer_class):
        entity_id = self.entity_service.get_entity_id(request)
        last_updated = request.GET.get('updated_at_gte')

        queryset = self.get_queryset(entity_id)
        if last_updated:
            queryset = queryset.filter(updated_at__gte=last_updated)

        queryset.order_by('updated_at')

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

class CommonMobileCreateMixin(object):

    def create_helper(self, request, serializer_class):
        entity_id = self.entity_service.get_entity_id(request)
        data = request.data
        data['entity'] = entity_id
        data['employee'] = data.get('employee') or request.user.id #Employee id is the same as user id
        serializer = serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommonMobileUpdateMixin(object):

    def update_helper(self, request, pk, serializer_class):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        object = get_object_or_404(queryset, pk=pk)

        #Validation
        new_global_last_changed = request.data.get('global_last_changed', False)

        if not new_global_last_changed:
            return Response({'error': 'global_last_changed required'}, status=status.HTTP_400_BAD_REQUEST)

        if parse_date(new_global_last_changed) < object.global_last_changed:
            return Response(serializer_class(object).data)

        #Main Logic
        serializer = serializer_class(object, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommonCrudMixin(CommonListMixin, CommonCreateMixin, CommonRetrieveMixin, CommonUpdateMixin, CommonDestroyMixin):
    pass

class CommonExtensionMixin(CommonTaskMixin, CommonEventMixin, CommonNoteMixin, CommonTimelineMixin):
    pass

class CustomerExtensionMixin(CommonExtensionMixin, CommonDealMixin):
    pass

class AccountExtensionMixin(CommonExtensionMixin, CommonDealMixin):
    pass

class ActionExtensionMixin(CommonCompanyMixin, CommonContactMixin, CommonNoteMixin):
    pass

class CommonMobileCrudMixin(CommonMobileSyncMixin, CommonMobileCreateMixin, CommonMobileUpdateMixin):
    pass