
from django.contrib import admin

from .models import Comment, Group, GroupRequest, Like, Member, Post, Replies
# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "privacy_status", "date_created", ]


class MemberAdmin(admin.ModelAdmin):
    list_display = ["is_admin", "is_suspended"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "is_hidden", "date_created"]


admin.site.register(Group, GroupAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Replies)
admin.site.register(Post)
admin.site.register(GroupRequest)
admin.site.register(Member, MemberAdmin)
