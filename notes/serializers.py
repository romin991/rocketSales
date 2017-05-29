from rest_framework import serializers
from notes.models import *

class NoteRelationSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)

    class Meta:
        model = Note

class NoteSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source="employee.user.first_name", read_only=True)
    employee_last_name = serializers.CharField(source="employee.user.last_name", read_only=True)
    employee_prof_pic = serializers.CharField(source="employee.prof_pic", read_only=True)

    class Meta:
        model = Note

class NoteMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note

class NoteMobileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        extra_kwargs = {'id': {'read_only': False, 'required': True}, 'global_last_changed': {'required': True}}