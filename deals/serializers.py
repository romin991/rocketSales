from rest_framework import serializers
from deals.models import *
from tasks.serializers import *
from notes.serializers import *
from events.serializers import *

class DealSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    customer_first_name = serializers.CharField(source='customer.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.last_name', read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Deal
        exclude = ('description', 'lost_note')

class DealAlgoliaSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    customer_first_name = serializers.CharField(source='customer.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.last_name', read_only=True)
    customer_email = serializers.CharField(source='customer.email')
    customer_phone = serializers.CharField(source='customer.phone')
    company_name = serializers.CharField(source="company.name", read_only=True)
    objectID = serializers.UUIDField(source='id')
    epoch_expected_closing_date = serializers.IntegerField(source='get_expected_closing_date')
    epoch_created_at = serializers.IntegerField(source='get_epoch_created_at')

    class Meta:
        model = Deal

class DealFullSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    customer_first_name = serializers.CharField(source='customer.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.last_name', read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Deal

class DealMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal

class DealMobileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal
        extra_kwargs = {'id': {'read_only': False, 'required': True}, 'global_last_changed': {'required': True}}

class DealMobileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        extra_kwargs = {'global_last_changed': {'required': True}}