from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import EmailConfirmation
from .serializers import (
    RegistrationSerializer, 
    ConfirmationSerializer, 
    LoginSerializer
)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_active=False
            )
            code = EmailConfirmation.generate_code()
            EmailConfirmation.objects.create(
                user=user,
                code=code
            )
            return Response(
                data={
                    'message': 'Пользователь успешно зарегистрирован!',
                    'user_id': user.id,
                    'username': user.username,
                    'confirmation_code': code  
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmationAPIView(APIView):
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            confirmation = serializer.validated_data['confirmation']
            user.is_active = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                data={
                    'message': 'Пользователь успешно подтвержден!',
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            return Response(
                data={
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
