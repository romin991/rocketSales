from rest_framework import serializers
from companies.models import *
from deals.serializers import *
from tasks.serializers import *
from notes.serializers import *
from customers.serializers import *
from events.serializers import *
from bases.models import *

#TODO
#Add Tasks and Deal url
ADDRESS_LIST = map(lambda x: x.name, AddressMixin._meta.get_fields())
SHIPPING_ADDRESS_LIST = map(lambda x: x.name, ShippingAddressMixin._meta.get_fields())
EXTRA_CONTACT = ['secondary_phone', 'facebook', 'instagram', 'twitter']
EXTRA_INFO = ['employee_num', 'annual_revenue', 'description']

class CompanySerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)

    class Meta:
        model = Company
        exclude_list = [ADDRESS_LIST, SHIPPING_ADDRESS_LIST, EXTRA_CONTACT, EXTRA_INFO]
        flatten_exclude_list = [val for sublist in exclude_list for val in sublist]
        exclude = flatten_exclude_list

class CompanyAlgoliaSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name")
    employee_last_name = serializers.CharField(source="employee.user.last_name")
    objectID = serializers.UUIDField(source='id')
    epoch_created_at = serializers.IntegerField(source='get_epoch_created_at')

    class Meta:
        model = Company

class CompanyFullSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    active_customers = CustomerSerializer(many=True, read_only=True)

    class Meta:
        model = Company

class CompanyMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

class CompanyMobileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        extra_kwargs = {'id': {'read_only': False, 'required': True}, 'global_last_changed': {'required': True}}

class CompanyMobileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        extra_kwargs = {'global_last_changed': {'required': True}}