from rest_framework_jwt.utils import jwt_payload_handler
from employees.models import *

def jwt_custom_payload_handler(user):
    payload = jwt_payload_handler(user)
    entity_id = Membership.objects.filter(is_deleted=False).filter(employee=user.employee).first().entity.id
    payload['entity_id'] = str(entity_id)
    payload['exp'] = Entity.objects.get(id=entity_id).expired.replace(tzinfo=None)
    return payload