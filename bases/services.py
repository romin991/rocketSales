from  rest_framework_jwt.utils import jwt_decode_handler


class EntityService(object):
    def __init__(self):
        self.__entity_id = ''

    def get_entity_id(self, request):
        if self.__entity_id != '':
            return self.__entity_id

        payload = jwt_decode_handler(request._auth)
        entity_id = payload['entity_id']
        self.__entity_id = entity_id
        return self.__entity_id