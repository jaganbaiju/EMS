from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
    path('form-create/', views.CreateDynamicFormView.as_view()),
    path('form-field/', views.FormFieldView.as_view()),
    path('employee/', views.EmployeeCreateView.as_view()),
    path('user-delete/', views.UserView.as_view()),
]


