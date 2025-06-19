from django.urls import path
from .views import registration, verify_otp

urlpatterns = [
    path('registr/', registration, name='registr'), 
    path('verify/', verify_otp, name='verify')
]