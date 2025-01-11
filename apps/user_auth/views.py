from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from ..users.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response("User created successfully!", status=status.HTTP_201_CREATED, headers=headers)
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        
        return Response({
            'access': str(access_token),
            'refresh': str(refresh_token)
        })
