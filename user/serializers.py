from rest_framework import serializers
from .models import User, Otp, Admin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'email']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['id', 'otp_key', 'otp_code']

class ResendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['id', 'otp_key']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)