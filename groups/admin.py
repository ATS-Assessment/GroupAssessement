from django.contrib import admin

from .models import Comment, Group, GroupRequest, Like, Member, Post, Replies

# Register your models here.
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Replies)
admin.site.register(Post)
admin.site.register(GroupRequest)
admin.site.register(Member)
