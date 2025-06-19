from django.urls import path
from .views import dd

urlpatterns = [
    path('', dd)
]