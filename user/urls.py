from django.urls import path
from .serializers import LoginSerializer
from .views import (registration, verify_otp, login_user, login_admin, resend_otp, chenge_password,
                    forgot_password, update_password)

urlpatterns = [
    path('registr/', registration, name='registr'), 
    path('verify/', verify_otp, name='verify'),
    path('login_admin/', login_admin, name='login_admin'),
    path('login_user/', login_user, name='login_user'),
    path('resend_otp/', resend_otp, name='resend_otp'),
    path('chenge_password/', chenge_password, name='chenge_password'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('update_password/', update_password, name='update_password'),
]