from django.contrib import admin
from .models import User, Otp, Admin
from django.contrib.auth.hashers import make_password


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_verify')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_verify',)
    ordering = ('-created_at',)


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'otp_key', 'created_at')
    search_fields = ('user__username', 'otp_code')
    list_filter = ('created_at',)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'status')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
