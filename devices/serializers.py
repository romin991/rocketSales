from rest_framework import serializers
from devices.models import *

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device