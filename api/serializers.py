from rest_framework import serializers
from .models import User, Request, Upload, Dispense

from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)
        
        
# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = "__all__"
        

class RequestSerializer(serializers.ModelSerializer): 
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    
    class Meta:
        model = Request
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        client = User.objects.get(pk=representation['client'])
        representation['client'] = {
            "id": client.id,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "phone_number": client.phone_number,
            "id_card_number": client.id_card_number
        }
        return representation
    
        
class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = "__all__"
        
        
class DispenseSerializer(serializers.ModelSerializer):

    request = serializers.PrimaryKeyRelatedField(queryset=Request.objects.all())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = Request.objects.get(pk=representation['request'])
        client = User.objects.get(pk=request.client.pk)

        representation['request'] = {
            'id': request.pk,
            'service': request.requested_service,
            'client': f"{client.first_name} {client.last_name}"
        }

        return representation

    class Meta: 
        model = Dispense
        fields = "__all__"


class StatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(write_only=True, required=True)