from django.contrib import admin

# Register your models here.
from poll.models import Poll

admin.site.register(Poll)
