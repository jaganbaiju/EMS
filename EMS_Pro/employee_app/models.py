from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class DynamicFormModel(models.Model):
    name = models.CharField(max_length=150)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



