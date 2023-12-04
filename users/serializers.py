from rest_framework import serializers
from .models import User, UserManager
from django.contrib import auth


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=15, min_length=8)
    password_confirm = serializers.CharField(write_only=True, max_length=15, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'])
        password = self.validated_data['password']

        if not user.password.isalnum():
            raise serializers.ValidationError("Password must consist of letters and numbers.")


       # contains_special = any(c in string.punctuation for c in password)
        if not user.password.string.punctuation():
            raise serializers.ValidationError("Password must consist of letters, numbers and symbols.")

        user.set_password(password)
        user.save()


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=15, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username, password=password)

        return {
            'username': user.username,
            'tokens': user.tokens()
        }
