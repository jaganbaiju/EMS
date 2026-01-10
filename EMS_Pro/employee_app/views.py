from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, DynamicFormSerializer, FormFieldSerializer, EmployeeSerializer
from rest_framework import status
from .models import DynamicFormModel, FormFieldModel, Employee
from django.shortcuts import get_object_or_404


# api for register user
class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'user registered successfully'})
        
        return Response(serializer.error, status=400)


# api for user profile
class UserProfileView(APIView):
    # authentication checking
    permission_classes = [IsAuthenticated]

    def get(self, request): 

        user = request.user

        return Response({
            'username': user.username,
            'email': user.email,
        })
    

# change password
class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully"})
    

# create dynamic form
class CreateDynamicFormView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        all_forms = DynamicFormModel.objects.filter(created_by=user)

        serializer = DynamicFormSerializer(all_forms, many=True)

        return Response({'all_forms': serializer.data})

    def post(self, request):
        user = request.user

        serializer = DynamicFormSerializer(data= request.data,
                                           context={'request': request})
        
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Dynamic form Created"},
                            status=status.HTTP_200_OK)
        
        return Response({serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


# create form field

class FormFieldView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        form_id = request.data.get('form')
        form = DynamicFormModel.objects.get(id=form_id)

        label = request.data.get('label')
        field_type = request.data.get('field_type')

        last_order = FormFieldModel.objects.filter(form=form).count()
        order= last_order + 1

        new_field = FormFieldModel.objects.create(
            form = form,
            label = label,
            field_type = field_type,
            order = order
        )

        new_field.save()


        return Response(
                {"message": "Field added successfully"},
                status=status.HTTP_201_CREATED
            )
    

    def get(self, request):
        form_id = request.query_params.get('id')

        if not form_id:
            return Response(
                {"error": "form name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        form = get_object_or_404(DynamicFormModel, id=form_id)
        fields = FormFieldModel.objects.filter(form=form).order_by('order')

        serializer = FormFieldSerializer(fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        
        form_id = data.get('form')

        if not form_id:
            return Response(
                {"error": "form is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            form_obj = DynamicFormModel.objects.get(id=form_id)
        except DynamicFormModel.DoesNotExist:
            return Response(
                {"error": "Invalid form name"},
                status=status.HTTP_400_BAD_REQUEST
            )


        data['form'] = form_obj

        # serializer = EmployeeSerializer(data=data)

        # if serializer.is_valid():
        #     serializer.save()
        emp = Employee.objects.create(form=data['form'], data=data['data'])
        emp.save()

        return Response(
                {
                    "message": "Employee created successfully",
                },
                status=status.HTTP_201_CREATED
            )

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user_id = request.query_params.get('id')

        if not user_id:
            return Response(
                {"error": "username is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)

        dynamic_forms = DynamicFormModel.objects.filter(created_by=user)

        serializer = DynamicFormSerializer(dynamic_forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_id = int(request.query_params.get('id'))
        user = get_object_or_404(User, id = user_id)
        user.delete()
        return Response({
            "message": "User deleted successfully"
        }, status=status.HTTP_200_OK)

    def get(self, request):
        user_id = int(request.query_params.get('id'))
        user = get_object_or_404(User, id = user_id)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_200_OK)
    
    def put(self, request):
        user_id = int(request.query_params.get('id'))
        user = get_object_or_404(User, id = user_id)

        user.username = request.data.get('username')
        user.email = request.data.get('email')

        user.save()

        return Response({"message": "user data updated"},
                        status=status.HTTP_200_OK)