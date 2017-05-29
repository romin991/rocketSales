from rest_framework import serializers
from tasks.models import *
from notes.serializers import *

class TaskSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    contact_first_name = serializers.CharField(source='contact_object.first_name', read_only=True)
    contact_last_name = serializers.CharField(source='contact_object.last_name', read_only=True)

    class Meta:
        model = Task
        exclude = ('description',)

#Everything is readonly
class TaskAlgoliaSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name")
    employee_last_name = serializers.CharField(source="employee.user.last_name")
    objectID = serializers.UUIDField(source='id')
    contact_first_name = serializers.CharField(source='contact_object.first_name')
    contact_last_name = serializers.CharField(source='contact_object.last_name')
    contact_email = serializers.CharField(source='contact_object.email')
    contact_phone = serializers.CharField(source='contact_object.phone')
    company_name = serializers.CharField(source='company.name')
    deal_name = serializers.CharField(source='deal.name')
    epoch_due_date = serializers.IntegerField(source='get_epoch_due_date')
    epoch_created_at = serializers.IntegerField(source='get_epoch_created_at')

    class Meta:
        model = Task

class TaskFullSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    contact_first_name = serializers.CharField(source='contact_object.first_name', read_only=True)
    contact_last_name = serializers.CharField(source='contact_object.last_name', read_only=True)
    company_name = serializers.CharField(source='get_company_name', read_only=True)
    deal_name = serializers.CharField(source='deal.name', read_only=True)

    class Meta:
        model = Task

class TaskMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task

class TaskMobileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        extra_kwargs = {'id': {'read_only': False, 'required': True}, 'global_last_changed': {'required': True}}

class TaskMobileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        extra_kwargs = {'global_last_changed': {'required': True}}