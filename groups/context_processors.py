

# from groups.decorators import is_member_of_group, not_suspended_member
# from .models import Group, Member, Post, Member, Like, Replies, GroupRequest, Comment
# from django.contrib.auth.models import User
# from django.http import HttpResponseRedirect, JsonResponse
# from django.urls import reverse
# from django.db.models import Q
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
# from django.views.generic import ListView, DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
# from django.contrib import messages
# from .models import Group
# from .forms import CommentForm, GroupForm, PostForm, ReplyForm
# from notification.models import Notification


# # @ login_required(login_url='login')  # join with group_detail
# def create_post(request, group_pk):

#     group = Group.objects.get(pk=group_pk)
#     group_member = group.group_member.all().filter(member=request.user)
#     if group_member.is_suspended is False:
#         if request.method == "POST":
#             post_form = PostForm(request.POST, request.FILES)
#             if post_form.is_valid():
#                 title = post_form.cleaned_data.get("title")
#                 content = post_form.cleaned_data.get("content")
#                 post_image = post_form.cleaned_data.get("post_image")
#                 post_files = post_form.cleaned_data.get("post_files")
#                 post = Post.objects.create(
#                     title=title, content=content, post_image=post_image, post_files=post_files, group=group, member=request.user)
#                 post.save()
#                 messages.success(request, "Post was created Successfully!")
#                 return JsonResponse({"data": post})
#             else:
#                 context = {
#                     "post_form": post_form
#                 }
#                 messages.error(
#                     request, "Post Creation failed,Please try again!")
#                 return render(request, "groups/group_detail.html", context)
#         else:
#             post_form = PostForm()
#             context = {
#                 "post_form": post_form
#             }
#             return render(request, "groups/group_detail.html", context)
#     else:
#         return JsonResponse({"message": "Permission Denied",
#                              })
