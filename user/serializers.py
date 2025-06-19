from rest_framework import serializers
from .models import User, Otp, Admin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'email', 'is_verify']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['id', 'otp_key', 'otp_code']