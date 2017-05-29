from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from employees.utils import *
from companies.models import *
from rest_framework import status
from employees.tokens import *
import jwt
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from bases.services import *
from employees.serializers import *
from employees.permissions import *
from algolias.constants import *
from algolias.registration import algolia_engine
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset_confirm, password_reset_complete
from django.contrib.auth.forms import SetPasswordForm
from django.conf import settings
from django.db import transaction
# Create your views here.

class RegisterUser(APIView):

    @transaction.atomic
    def post(self, request, format=None):
        email = request.data.get('email', '')
        email = email.lower()
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        password = request.data.get('password', '')
        company_name = request.data.get('company', '')
        if (not EmployeeUtil.validate_email(email)):
            return Response({'status': 'Bad request', 'message': 'email is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 8:
            return Response({'status': 'Bad request', 'message': 'password minimum length is 8'}, status=status.HTTP_400_BAD_REQUEST)

        if (not EmployeeUtil.validate_email(email) or len(password) < 8 or first_name == ''
            or last_name == '' or company_name == ''):
            return Response({
                'status': 'Bad request',
                'message': 'Bad data'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = Account.objects.filter(email=email)
        if not user:

            new_user = Account.objects.create_user(username=email, email=email,password=password, first_name=first_name, last_name=last_name)
            new_employee = Employee.objects.create_employee(new_user)
            new_entity = Entity.objects.create_entity(company_name, expired=timezone.now()+timedelta(days=30))
            membership = Membership.objects.create_membership(new_employee, new_entity, role=EmployeeConstant.ADMIN)

            #Init algolia index
            # for algolia_model in AlgoliaConstant.MODEL_DICT.keys():
            #     index_name = algolia_model + str(new_entity.id)
            #     algolia_index = AlgoliaConstant.MODEL_DICT.get(algolia_model)
            #     algolia_engine.register(index_name, algolia_index)

            payload = jwt_custom_payload_handler(new_user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            return Response({'created':True, 'token': token}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Bad request', 'message': 'email existed'}, status=status.HTTP_400_BAD_REQUEST)

class Reset(APIView):

    def post(self, request, format=None):
        email = request.data.get('email', '')
        email = email.lower()
        users = Account.objects.filter(email=email)
        if len(users) == 0:
            return Response({'message':'invalid email'}, status=status.HTTP_401_UNAUTHORIZED)

        user = users[0]
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        context = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        email_template_name = 'employees/resetemail.html'
        subject_template_name = 'employees/resetsubject.html'
        send_mail(subject_template_name, email_template_name,
                  context, settings.EMAIL_ADDRESS, user.email)

        return Response({'send':True}, status=status.HTTP_201_CREATED)

class EmployeeViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ()

    def __init__(self, *args, **kwargs):
        super(EmployeeViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def list(self, request):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        filtered_queryset = self.filter_queryset(queryset)
        employee_serializer = EmployeeSerializer(filtered_queryset, many=True)

        return Response(employee_serializer.data)

    def retrieve(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        employee = get_object_or_404(queryset, pk=pk)
        employee_full_serializer = EmployeeFullSerializer(employee)

        return Response(employee_full_serializer.data)

    #Can only update self
    def update(self, request, pk=None):
        if str(request.user.id) != pk:
            return Response({'message':'Cannot update others'}, status=status.HTTP_400_BAD_REQUEST)
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        employee = get_object_or_404(queryset, pk=pk)
        employee_full_serializer = EmployeeFullSerializer(employee, data=request.data, partial=True)

        if employee_full_serializer.is_valid():
            employee_full_serializer.save()
            return Response(employee_full_serializer.data)
        return Response(employee_full_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #TODO
    #Update and destroy

    def get_queryset(self, entity_id):
        queryset = Employee.objects.filter(members=entity_id).filter(membership__is_deleted=False)
        return queryset


class MembershipViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, AdminPermission)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ()

    def __init__(self, *args, **kwargs):
        super(MembershipViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    #Not surpass the employee count
    @transaction.atomic
    def create(self, request):
        entity_id = self.entity_service.get_entity_id(request)
        data = request.data
        data['entity_id'] = entity_id
        create_membership_serializer = CreateMemberShipSerializer(data=data)

        if not create_membership_serializer.is_valid():
            return Response(create_membership_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = create_membership_serializer.data['email'].lower()
        exist_memberships = Membership.objects.filter(entity_id=entity_id).filter(employee__user__email=email)

        role = create_membership_serializer.data.get('role') or EmployeeConstant.EMPLOYEE

        #Check if user reactivate the deactivate account
        if len(exist_memberships) == 0 :
            first_name = create_membership_serializer.data['first_name']
            last_name = create_membership_serializer.data['last_name']

            new_user = Account.objects.create_user(username=email, email=email,password=Account.objects.make_random_password(),
                                                first_name=first_name, last_name=last_name)
            new_employee = Employee.objects.create_employee(new_user)
            Membership.objects.create_membership(new_employee, Entity.objects.get(id=entity_id), role=role)
        else:
            membership = exist_memberships.first()
            new_user = membership.employee.user
            membership.is_deleted = False
            membership.role = role
            new_user.is_active = True
            membership.save()
            new_user.save()

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        context = {
            'email': new_user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'user': new_user,
            'token': default_token_generator.make_token(new_user),
            'protocol': 'http',
        }

        email_template_name = 'employees/activationemail.html'
        subject_template_name = 'employees/activationsubject.html'
        send_mail(subject_template_name, email_template_name,
                  context, settings.EMAIL_ADDRESS, new_user.email)
        return Response({'created':True}, status=status.HTTP_201_CREATED)

    def list(self, request):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        filtered_queryset = self.filter_queryset(queryset)
        membership_serializer = MembershipSerializer(filtered_queryset, many=True)

        return Response(membership_serializer.data)

    #Cannot update self
    def update(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        membership = Membership.objects.filter(is_deleted=False).filter(employee=request.user.id).filter(entity=entity_id).first()
        if str(membership.id) == pk:
            return Response({'message':'Cannot self update'}, status=status.HTTP_400_BAD_REQUEST)
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        membership = get_object_or_404(queryset, pk=pk)
        membership_serializer = MembershipSerializer(membership, data=request.data, partial=True)

        if membership_serializer.is_valid():
            membership_serializer.save()
            return Response(membership_serializer.data)
        return Response(membership_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        entity_id = self.entity_service.get_entity_id(request)
        membership = Membership.objects.filter(is_deleted=False).filter(employee=request.user.id).filter(entity=entity_id).first()
        if str(membership.id) == pk:
            return Response({'message':'Cannot self update'}, status=status.HTTP_400_BAD_REQUEST)
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        membership = get_object_or_404(queryset, pk=pk)
        cur_employee = request.user.employee
        self.perform_destroy(membership, cur_employee)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def perform_destroy(self, membership, cur_employee):
        employee = membership.employee
        user = employee.user
        membership.is_deleted = True
        user.is_active = False
        membership.save()
        user.save()

        self.migrate_list(employee.active_leads(), cur_employee)
        self.migrate_list(employee.active_customers(), cur_employee)
        self.migrate_list(employee.active_companies(), cur_employee)

        self.migrate_list(employee.active_open_deals(), cur_employee)
        self.migrate_list(employee.active_open_tasks(), cur_employee)
        self.migrate_list(employee.active_open_events(), cur_employee)
        return

    def migrate_list(self, list, cur_employee):
        for obj in list:
            obj.employee = cur_employee
            obj.save()

    def get_queryset(self, entity_id):
        queryset = Membership.objects.filter(entity_id=entity_id).filter(is_deleted=False)
        return queryset


def activation_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, uidb64, token, set_password_form=SetPasswordForm,
                                  template_name='employees/activationconfirm.html', post_reset_redirect='activation_complete')

def activation_complete(request):
    return render(request, 'employees/activationemailcomplete.html')


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, uidb64, token, set_password_form=SetPasswordForm,
                                  template_name='employees/resetconfirm.html', post_reset_redirect='reset_complete')

def reset_complete(request):
    return render(request, 'employees/resetcomplete.html')


class MembershipMobileViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(MembershipMobileViewSet, self).__init__(*args, **kwargs)
        self.entity_service = EntityService()

    def list(self, request):
        entity_id = self.entity_service.get_entity_id(request)
        queryset = self.get_queryset(entity_id)
        membership_serializer = MembershipMobileSerializer(queryset, many=True)

        return Response(membership_serializer.data)

    def get_queryset(self, entity_id):
        queryset = Membership.objects.filter(entity_id=entity_id)
        return queryset