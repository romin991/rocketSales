from algolias.registration import algolia_engine
from algolias.constants import *
from django.conf import settings
from algoliasearch import algoliasearch

def register_algolia_update_signal(instance):
    index_config = AlgoliaConstant.MODEL_DICT.get(instance._meta.object_name)
    algolia_index = algolia_engine.get_algolia_index(instance, index_config)
    algolia_index.update_obj_index(instance)

def get_algolilas_meta(entity_id):
    params = getattr(settings, 'ALGOLIA', None)

    algolia_meta = {}
    index_list = []
    index_dict = {}
    for algolia_key in AlgoliaConstant.MODEL_DICT:
        index_name = algolia_key + str(entity_id)

        if 'INDEX_PREFIX' in params:
            index_name = params['INDEX_PREFIX'] + '_' + index_name
        if 'INDEX_SUFFIX' in params:
            index_name += '_' + params['INDEX_SUFFIX']

        index_list.append(index_name)
        index_dict[algolia_key.lower()] = index_name

    client = algoliasearch.Client(params['APPLICATION_ID'], params['API_KEY'])
    public_key = client.generate_secured_api_key(params['SEARCH_API_KEY'], {'restrictIndices': index_list})

    algolia_meta['index_dict'] = index_dict
    algolia_meta['application_id'] = params['APPLICATION_ID']
    algolia_meta['public_key'] = public_key

    return algolia_meta
