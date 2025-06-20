from django.urls import path

from .serializers import LoginSerializer
from .views import registration, verify_otp, resend_otp, login

urlpatterns = [
    path('registr/', registration, name='registr'), 
    path('verify/', verify_otp, name='verify'),
    path('resend/', resend_otp, name='resend'),
    path('login/', login, name='login'),
]