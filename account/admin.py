from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from account.models import User,UserProfile

class UserProfileAdmin(admin.StackedInline):
    list_display = ["profile_pix","phone_number","location"]
    model = UserProfile
class UserAdmin(BaseUserAdmin):
    filter_horizontal = ()
    list_filter = ()
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
    ordering = ('-date_joined',)
    fieldsets = ()
    inlines = [UserProfileAdmin]


admin.site.register(User, UserAdmin)

