from rest_framework import serializers
from entities.models import *
# Create your views here.
class EntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entity
