from rest_framework import serializers
from reports.models import *

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        extra_kwargs = {'status': {'read_only': True}, 'url': {'read_only': True},
                        'meta': {'read_only': True}}
        exclude = ('meta',)

class ReportFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        extra_kwargs = {'status': {'read_only': True}, 'url': {'read_only': True},
                        'meta': {'read_only': True}}