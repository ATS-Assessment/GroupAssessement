from poll.models import Poll, Choice, Voter
from django.contrib import admin
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'creator', 'group']}),
        ('Date information', {'fields': [
         'start_date', 'end_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Poll, PollAdmin)
admin.site.register(Voter)
