
from django.contrib import admin

from notification.models import Notification, Event

# Register your models here.

admin.site.register(Notification),
admin.site.register(Event)
# admin.site.register(Poll)
