from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DynamicFormModel, FormFieldModel, Employee


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
        fields = ['id', 'name']

    def validate_name(self, value):
        user = self.context['request'].user

        if DynamicFormModel.objects.filter(name=value,created_by=user).exists():
            raise serializers.ValidationError(
                "Form name already exists"
            )

        return value

    def create(self, validated_data):
        user = self.context['request'].user

        dynamicForm = DynamicFormModel.objects.create(
            name=validated_data['name'],
            created_by=user
        )

        return dynamicForm
    

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormFieldModel
        fields = ['id', 'form', 'label', 'field_type', 'order']
        extra_kwargs = {
            'order': {'required': False}
        }

    def validate(self, attrs):
        form = attrs.get('form')
        order = attrs.get('order')

        if order is not None:
            if FormFieldModel.objects.filter(form=form, order=order).exists():
                raise serializers.ValidationError(
                    "Field with this order already exists in the form"
                )

        return attrs

    def create(self, validated_data):

        forms = validated_data['form']

        form = FormFieldModel.objects.get(id=forms)

        if 'order' not in validated_data:
            last_order = FormFieldModel.objects.filter(form=form).count()
            validated_data['order'] = last_order + 1

        return super().create(validated_data)
    

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'form', 'data', 'created_at']