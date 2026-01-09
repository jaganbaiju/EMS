from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DynamicFormModel


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user
    

class DynamicFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicFormModel
        field = ['name']


    def create(self, validated_data):
        user = self.context['request'].user

        dynamicForm = DynamicFormModel.objects.create(
            name=validated_data['name'],
            created_by=user
        )

        return dynamicForm