from rest_framework import serializers
from events.models import *
from notes.serializers import *

ADDRESS_LIST = ['street', 'city', 'state', 'country', 'pos_code']
EXTRA_INFO = ['description']

class EventSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    contact_first_name = serializers.CharField(source='contact_object.first_name', read_only=True)
    contact_last_name = serializers.CharField(source='contact_object.last_name', read_only=True)

    class Meta:
        model = Event
        exclude_list = [ADDRESS_LIST, EXTRA_INFO]
        flatten_exclude_list = [val for sublist in exclude_list for val in sublist]
        exclude = flatten_exclude_list

#Everything is readonly
class EventAlgoliaSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name")
    employee_last_name = serializers.CharField(source="employee.user.last_name")
    objectID = serializers.UUIDField(source='id')
    contact_first_name = serializers.CharField(source='contact_object.first_name')
    contact_last_name = serializers.CharField(source='contact_object.last_name')
    contact_email = serializers.CharField(source='contact_object.email')
    contact_phone = serializers.CharField(source='contact_object.phone')
    company_name = serializers.CharField(source='company.name')
    deal_name = serializers.CharField(source='deal.name')
    epoch_start_time = serializers.IntegerField(source='get_epoch_start_time')

    class Meta:
        model = Event

class EventFullSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    contact_first_name = serializers.CharField(source='contact_object.first_name', read_only=True)
    contact_last_name = serializers.CharField(source='contact_object.last_name', read_only=True)
    company_name = serializers.CharField(source='get_company_name', read_only=True)
    deal_name = serializers.CharField(source='deal.name', read_only=True)

    class Meta:
        model = Event

class EventMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event

class EventMobileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        extra_kwargs = {'id': {'read_only': False, 'required': True}, 'global_last_changed': {'required': True}}

class EventMobileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        extra_kwargs = {'global_last_changed': {'required': True}}
