from django.contrib import admin
from .models import DynamicFormModel, FormFieldModel, Employee
# Register your models here.

admin.site.register(DynamicFormModel)
admin.site.register(FormFieldModel)
admin.site.register(Employee)