from django.conf import settings
from algoliasearch import algoliasearch
from algolias.models import AlgoliaIndex
from django.db.models.signals import post_save, pre_delete

def model_type(cls):
    return '%s' % (cls._meta.object_name)

class AlgoliaEngine(object):
    def __init__(self, app_id=None, api_key=None):
        params = getattr(settings, 'ALGOLIA', None)
        app_id = params['APPLICATION_ID']
        api_key = params['API_KEY']

        self.client = algoliasearch.Client(app_id, api_key)
        self.__registered_indexs = {}

    def get_algolia_index(self, instance, index_cls=AlgoliaIndex):
        model_str = model_type(instance)
        entity_id = instance.entity.id
        index_name = model_str + str(entity_id)
        if self.is_registered(index_name):
            return self.__registered_indexs[index_name]

        algolia_index = self.register(index_name, index_cls)
        return algolia_index

    def register(self, index_name, index_cls=AlgoliaIndex):
        algolia_index = index_cls(index_name, self.client)
        self.__registered_indexs[index_name] = algolia_index
        return algolia_index

    def is_registered(self, indexname):
        '''Checks whether the given models is registered with Algolia engine.'''
        return indexname in self.__registered_indexs

algolia_engine = AlgoliaEngine()