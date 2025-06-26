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

class ResendOTPSerializer(serializers.Serializer):
    class Meta:
        model = Otp
        fields = ['id', 'otp_key']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

class UpdatePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    otp_key = serializers.CharField(required=True)
    otp_code = serializers.IntegerField(required=True)