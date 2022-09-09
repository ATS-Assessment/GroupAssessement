from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from account.models import User


class UserAdmin(BaseUserAdmin):
    filter_horizontal = ()
    list_filter = ()
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
    ordering = ('-date_joined',)
    fieldsets = ()


admin.site.register(User, UserAdmin)
