from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class DynamicFormModel(models.Model):
    name = models.CharField(max_length=150)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class FormFieldModel(models.Model):
    FIELD_TYPES = (
        ('text', 'text'),
        ('number', 'number'),
        ('email', 'email'),
        ('date', 'date'),
        ('password', 'password')
    )

    form = models.ForeignKey(DynamicFormModel, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    field_type = models.CharField(
        max_length=50, 
        choices=FIELD_TYPES, 
        default='text'
        )
    order = models.IntegerField()

    def __str__(self):
        return self.label


class Employee(models.Model):
    form = models.ForeignKey(DynamicFormModel, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)