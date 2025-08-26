from rest_framework import serializers

class ConfigSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=120)
    value = serializers.CharField(max_length=255)
