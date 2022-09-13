from django.contrib import admin

from event.models import Event

# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "start_time",
                    "end_time"]


admin.site.register(Event, EventAdmin)
