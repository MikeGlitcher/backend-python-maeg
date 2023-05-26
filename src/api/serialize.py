from rest_framework import serializers

from ejercicios.models import ProductModels

class MenuSerializer(serializers.Serializer):
    task = serializers.CharField(required=True)



class BaseSerializer(serializers.Serializer):
    id_ = serializers.IntegerField(required=False)
    title = serializers.CharField(required=True)
    price = serializers.FloatField(required=True)
    description = serializers.CharField(required=True)
    color = serializers.CharField(required=True)



class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductModels
        fields  = ["id", "title", "price"]