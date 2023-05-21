from rest_framework import serializers

class FunctionSerializer(serializers.Serializer):
    id_ = serializers.IntegerField(required=False)

class BaseSerializer(serializers.Serializer):
    id_ = serializers.IntegerField(required=False)
    product = serializers.CharField(required=True)
    price = serializers.FloatField(required=True)
    description = serializers.CharField(required=True)
    color = serializers.CharField(required=True)

class CreateSerializer(serializers.Serializer):
    product = serializers.CharField(required=True)
    price = serializers.FloatField(required=True)
    description = serializers.CharField(required=True)
    color = serializers.CharField(required=True)