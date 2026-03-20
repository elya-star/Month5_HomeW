from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import EmailConfirmation

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)  

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует!')
        return username
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует!')
        return email


class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data.get('username')
        code = data.get('code')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError({'username': 'Пользователь не найден!'})
        
        try:
            confirmation = EmailConfirmation.objects.get(user=user)
        except EmailConfirmation.DoesNotExist:
            raise ValidationError({'code': 'Код подтверждения не найден!'})
        
        if confirmation.code != code:
            raise ValidationError({'code': 'Неверный код подтверждения!'})
        
        data['user'] = user
        data['confirmation'] = confirmation
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        
        if not user:
            raise ValidationError('Неверное имя пользователя или пароль!')
        
        if not user.is_active:
            raise ValidationError('Аккаунт не активирован! Подтвердите email.')
        
        data['user'] = user
        return data