from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer
from rest_framework import status


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