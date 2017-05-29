from rest_framework import serializers
from leads.models import *
from tasks.serializers import *
from notes.serializers import *
from events.serializers import *

#TODO
#Add Tasks url

ADDRESS_LIST = map(lambda x: x.name, AddressMixin._meta.get_fields())
EXTRA_CONTACT = ['secondary_phone', 'secondary_mobile_phone', 'fax', 'skype','line', 'facebook', 'instagram', 'twitter']
EXTRA_INFO = ['birth_date', 'description']

class LeadSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)

    class Meta:
        model = Lead
        exclude_list = [ADDRESS_LIST, EXTRA_CONTACT, EXTRA_INFO]
        flatten_exclude_list = [val for sublist in exclude_list for val in sublist]
        exclude = flatten_exclude_list

#Everything is readonly
class LeadAlgoliaSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name")
    employee_last_name = serializers.CharField(source="employee.user.last_name")
    objectID = serializers.UUIDField(source='id')
    epoch_created_at = serializers.IntegerField(source='get_epoch_created_at')

    class Meta:
        model = Lead

class LeadFullSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    converted_customer = serializers.PrimaryKeyRelatedField(read_only=True)
    converted_customer_first_name = serializers.CharField(source="converted_customer.first_name", read_only=True)
    converted_customer_last_name = serializers.CharField(source="converted_customer.last_name", read_only=True)

    class Meta:
        model = Lead

class LeadMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead

class LeadMobileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        extra_kwargs = {'id': {'read_only': False, 'required': True}, 'global_last_changed': {'required': True}}


class LeadMobileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        extra_kwargs = {'global_last_changed': {'required': True}}