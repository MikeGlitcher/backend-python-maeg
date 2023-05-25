from rest_framework import serializers

class MenuSerializer(serializers.Serializer):
    task = serializers.CharField(required=True)

class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(required=True)

class BaseSerializer(serializers.Serializer):
    id_ = serializers.IntegerField(required=False)
    title = serializers.CharField(required=True)
    price = serializers.FloatField(required=True)
    description = serializers.CharField(required=True)
    color = serializers.CharField(required=True)

