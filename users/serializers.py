from rest_framework import serializers
from .models import User, UserManager
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=15, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


#class EmailVerificationSerializer(serializers.ModelSerializer):
   # token = serializers.CharField(min_length=555)

    #class Meta:
        #model = User
        #fields = ['token']


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

        # if not user:
        #     raise AuthenticationFailed('Invalid username or password, try again')
        # if not user.password_validator:
        #     raise AuthenticationFailed('Invalid password, try again')
    #     if not user.is_active:
    #         raise AuthenticationFailed('Account disabled, contact admin')
    #     if not user.is_verified:
    #         raise AuthenticationFailed('Email is not verified')
        return {
            'username': user.username,
            'tokens': user.tokens()
        }




    # def logout(self):
    #     pass
   # refresh = serializers.CharField()
   #
   #  default_error_messages = {
   #     'bad_token': 'Token is expired or invalid'
   #  }
   #  def validate(self, attrs):
   #     self.token = attrs['refresh']
   #
   #  return attrs
   #
   #  def save(self, **kwargs):
   #
   #      try:
   #          RefreshToken(self.token).blacklist()
   #
   #      except TokenError:
   #          self.fail('bad_token')

