from __future__ import unicode_literals
from django.conf import settings

from django.db import models

# Create your models here.
class AlgoliaIndex(object):

    serializer = None

    tags = None

    settings = {}

    def __init__(self, index_name, client):
        '''Initializes the index.'''
        self.index_name = index_name
        self.__client = client
        self.__set_index(client)
        self.__set_settings()

    def __set_index(self, client):
        params = getattr(settings, 'ALGOLIA', None)

        if params:
            if 'INDEX_PREFIX' in params:
                self.index_name = params['INDEX_PREFIX'] + '_' + self.index_name
            if 'INDEX_SUFFIX' in params:
                self.index_name += '_' + params['INDEX_SUFFIX']
        self.__index = client.init_index(self.index_name)

    def __set_settings(self):
        '''Apply the settings to the index.'''
        if self.settings:
            self.__index.set_settings(self.settings)

    def update_obj_index(self, instance):
        serializer =self.serializer(instance)
        self.__index.save_object(serializer.data)

    def delete_obj_index(self, instance):
        objectID = instance.pk
        self.__index.delete_object(objectID)