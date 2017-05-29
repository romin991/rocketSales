from rest_framework import serializers
from customers.models import *
from tasks.serializers import *
from notes.serializers import *
from deals.serializers import *
from events.serializers import *

ADDRESS_LIST = map(lambda x: x.name, AddressMixin._meta.get_fields())
EXTRA_CONTACT = ['secondary_phone', 'secondary_mobile_phone', 'fax', 'skype','line', 'facebook', 'instagram', 'twitter']
EXTRA_INFO = ['birth_date', 'description']

class CustomerSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Customer
        exclude_list = [ADDRESS_LIST, EXTRA_CONTACT, EXTRA_INFO]
        flatten_exclude_list = [val for sublist in exclude_list for val in sublist]
        exclude = flatten_exclude_list

class CustomerAlgoliaSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name")
    employee_last_name = serializers.CharField(source="employee.user.last_name")
    objectID = serializers.UUIDField(source='id')
    company_name = serializers.CharField(source='company.name')
    epoch_created_at = serializers.IntegerField(source='get_epoch_created_at')

    class Meta:
        model = Customer

class CustomerFullSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    lead_origin_first_name = serializers.CharField(source="lead_origin.first_name", read_only=True)
    lead_origin_last_name = serializers.CharField(source="lead_origin.last_name", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Customer

class CustomerMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer

class CustomerMobileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        extra_kwargs = {'id': {'read_only': False, 'required': True}, 'global_last_changed': {'required': True}}

class CustomerMobileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        extra_kwargs = {'global_last_changed': {'required': True}}