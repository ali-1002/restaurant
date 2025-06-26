from uuid import uuid4
from django.db import models

ADMIN_STATUS = (
    (0, 'Blocked'),
    (1, 'Active')
)


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(unique=True, null=True)
    role = models.CharField(default='user', max_length=20)
    is_verify = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.PositiveIntegerField()
    otp_key = models.UUIDField(default=uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"


class Admin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    passport_number = models.CharField(max_length=9, unique=True)
    personal_number = models.CharField(max_length=14, unique=True) 
    role = models.CharField(default='admin')
    status = models.IntegerField(choices=ADMIN_STATUS, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'admin'
        verbose_name = "Admin"
        verbose_name_plural = "Admins"