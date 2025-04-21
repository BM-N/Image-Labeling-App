from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Images, Labels

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {"write_only":True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["id", "image", "uploaded_by"]
        extra_kwargs = {"uploaded_by":{"read_only":True}}


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ["id", "label", "image_id","image", "confidence"]