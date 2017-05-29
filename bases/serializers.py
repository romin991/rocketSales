from rest_framework import serializers

class SendMessageSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False)
    phone = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    message = serializers.CharField(required=True, allow_blank=False)