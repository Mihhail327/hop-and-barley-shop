from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class MyUserAdmin(UserAdmin):
    # Указываем, какие поля отображать в списке
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']
    # Поиск по почте и имени
    search_fields = ['email', 'username']
    ordering = ['email']
