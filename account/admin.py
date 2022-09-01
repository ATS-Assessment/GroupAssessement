from django.contrib import admin

# Register your models here.
from account.models import UserProfile, UserGroup, Admin

admin.site.register(UserProfile)
admin.site.register(UserGroup)
admin.site.register(Admin)