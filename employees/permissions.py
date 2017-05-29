from rest_framework import permissions
from rest_framework_jwt.utils import jwt_decode_handler
from employees.models import *
class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        entity_id = jwt_decode_handler(request._auth)['entity_id']
        membership = Membership.objects.filter(entity_id=entity_id).filter(employee_id=request.user.pk).first()
        if membership.role == EmployeeConstant.ADMIN:
            return True

        return False