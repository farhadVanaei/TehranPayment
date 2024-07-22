from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'phone_number', 'is_staff', 'is_superuser')
    search_fields = ('username', 'phone_number')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
