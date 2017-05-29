from rest_framework import serializers
from employees.models import *
from tasks.serializers import *
from notes.serializers import *
from deals.serializers import *



class UserEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'email')
        read_only_fields = ('email',)

class EmployeeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    email = serializers.CharField(source="user.email", required=False)

    class Meta:
        model = Employee
        exclude = ('members',)


class EmployeeFullSerializer(serializers.ModelSerializer):
    user = UserEmployeeSerializer(required=False)

    class Meta:
        model = Employee

    def update(self, instance, validated_data):
        if validated_data.get('user') != None:
            user = instance.user
            user_data = validated_data.pop('user')
            user = super(EmployeeFullSerializer, self).update(user, user_data)
        instance = super(EmployeeFullSerializer, self).update(instance, validated_data)
        return instance

class MembershipSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="employee.user.first_name", required=False, read_only=True)
    last_name = serializers.CharField(source="employee.user.last_name", required=False, read_only=True)
    email = serializers.EmailField(source="employee.user.email", required=False, read_only=True)

    class Meta:
        model = Membership
        fields = ('id', 'email', 'first_name','last_name', 'created_at', 'updated_at', 'role')

class CreateMemberShipSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    entity_id = serializers.UUIDField(required=True)
    role = serializers.CharField(required=False)

    #make sure not exist and not more than entity max user
    def validate(self, data):
        entity_id = data['entity_id']
        email = data['email'].lower()
        memberships = Membership.objects.filter(entity_id=entity_id).filter(employee__user__email=email).filter(is_deleted=False)
        if len(memberships) != 0 :
            raise serializers.ValidationError("Email existed")

        user_count = len(Membership.objects.filter(entity_id=entity_id).filter(is_deleted=False))
        max_user = Entity.objects.get(id=entity_id).max_user
        if user_count >= max_user:
            raise serializers.ValidationError("Quota exceed")

        return data

class MembershipMobileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="employee.user.first_name", required=False, read_only=True)
    last_name = serializers.CharField(source="employee.user.last_name", required=False, read_only=True)
    email = serializers.EmailField(source="employee.user.email", required=False, read_only=True)

    class Meta:
        model = Membership
