

from groups.decorators import is_member_of_group, not_suspended_member
from .models import Group, Member, Post, Member, Like, Replies, GroupRequest, Comment
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Group
from .forms import CommentForm, GroupForm, PostForm, ReplyForm
from notification.models import Notification

# Create your views here.


class GroupList(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_list.html"
    context_object_name = "group_list"


def group_list(request):
    groups = Group.objects.all()

# class GroupDetail(LoginRequiredMixin, DetailView):
#     model = Group
#     template_name = "groups/group_detail.html"
#     context_object_name = "group"


@login_required(login_url='login')
def group_detail(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    group_posts = Post.visible_objects.filter(
        group__pk=group_pk).order_by('-date_created')
    context = {
        "group": group,
        "members": group.group_member.all(),
        "count": group.group_member.all().count(),
        "member": Member.objects.all(),
    }
    for post in group_posts:
        post_comments = Comment.objects.complex_filter(
            post__pk=post.pk).order_by('-date_created')
        for comment in post_comments:
            comment_replies = Replies.objects.filter(
                comment__pk=comment.pk).order_by('-date_created')
            context["post_comments"] = post_comments
            context["comment_replies"] = comment_replies
            context["group_post"] = group_posts

    return render(request, "groups/group_detail.html", context)


@ login_required(login_url='login')
def create_group(request):
    if request.method == "POST":
        group_form = GroupForm(request.POST, request.FILES)
        if group_form.is_valid():
            name = group_form.cleaned_data.get("name")
            description = group_form.cleaned_data.get("description")
            privacy_status = group_form.cleaned_data.get("privacy_status")
            group_image = group_form.cleaned_data.get("group_image")
            group = Group.objects.create(
                name=name, description=description, privacy_status=privacy_status, creator=request.user, group_image=group_image)
            new_member = Member.objects.create(
                group=group, member=group.creator, is_admin=True)
            print(new_member.member)
            group.save()
            new_member.save()
            messages.success(
                request, f"Your new Group {group.name} was successfully created! and {group.creator} is the Admin")
            return redirect("group-list")
        else:
            messages.error(
                request, "Group Creation failed, Please try again!")
            return render(request, "groups/group_create.html", {
                "group_form": group_form
            })
    else:
        group_form = GroupForm(request.POST)
        return render(request, "groups/group_create.html", {
            "group_form": group_form
        })


@ require_POST
@ login_required(login_url="login")
def make_admin(request, group_pk, admin_pk, user_pk):
    group = Group.objects.filter(
        pk=group_pk, creator__pk=admin_pk).first()
    if group.group_member.all().filter(is_admin=True).count() < 3:
        member = Member.objects.get(user__pk=user_pk)
        member.is_admin = True
        member.save()
        messages.success(
            request, f"{member.user.first_name} has successfully been made an Admin!")
        return redirect(request.META["HTTP_REFERER"])
    else:
        messages.error(
            request, "Group Admins cannot be more than 3!")
        return redirect(request.META["HTTP_REFERER"])


@require_POST
@login_required(login_url='login')
def remove_group_member(request, group_pk, admin_pk, user_pk):
    group = Group.objects.filter(
        pk=group_pk, creator__pk=admin_pk)
    member = group.group_member.filter(user__pk=user_pk)
    member.has_exited = True
    member.save()
    messages.success(
        request, f"{member.user.first_name} has successfully been removed from the Group!")
    return redirect(request.META["HTTP_REFERER"])


@ login_required(login_url='login')
def request_to_join_group(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    group_request = GroupRequest.objects.create(
        user=request.user, group=group)
    # admins = group.group_member.all().filter(member__is_admin=True)
    # for admin in admins:
    Notification.objects.create(group=group,
                                notification_type="group_request", is_admin_notification=True)
    return redirect(request.META["HTTP_REFERER"])


def request_add(request, group_pk, user_pk):

    group = Group.objects.get(pk=group_pk)
    user = User.objects.get(pk=user_pk)
    new_member = Member.objects.create(
        group=group, member=user)
    return redirect(reverse('group-detail', args=[group_pk]))


def request_reject_():
    pass


@login_required(login_url="login")
def accept_to_group(request):
    member = request.user.user_member
    if member.is_admin:
        pass


@require_POST
@ login_required(login_url='login')
def exit_group(request, group_name, user_pk):
    group = Group.objects.get(name=group_name)
    member = group.group_member.filter(user__pk=user_pk)
    member.has_exited = True
    member.save()
    member.save()
    messages.success(
        request, f"{member.user.first_name} has successfully exited from the Group!")
    return redirect("group-list")


def suspend_member(request, group_name, admin_pk, user_pk):
    group = Group.objects.get(name=group_name, user__pk=admin_pk).first()
    member = group.group_member.filter(user__pk=user_pk)
    member.is_suspended = True
    member.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@is_member_of_group
@ login_required(login_url='login')  # join with group_detail
def create_post(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    group_member = group.group_member.all().filter(member=request.user)
    if group_member.is_suspended is False:
        if request.method == "POST":
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                title = post_form.cleaned_data.get("title")
                content = post_form.cleaned_data.get("content")
                post_image = post_form.cleaned_data.get("post_image")
                post_files = post_form.cleaned_data.get("post_files")
                post = Post.objects.create(
                    title=title, content=content, post_image=post_image, post_files=post_files, group=group, member=request.user)
                post.save()
                messages.success(request, "Post was created Successfully!")
                return JsonResponse({"data": post})
            else:
                context = {
                    "post_form": post_form
                }
                messages.error(
                    request, "Post Creation failed,Please try again!")
                return render(request, "post_create.html", context)
        else:
            context = {
                "post_form": post_form
            }
            return render(request, "post_create.html", context)
    else:
        return JsonResponse({"message": "Permission Denied",
                             })


@login_required(login_url="login")
def search_groups(request):
    if request.method == 'POST':
        group_name = request.POST.get('search')
        print(group_name)
        results = Group.objects.filter(
            Q(name__icontains=group_name) | Q
            (description__icontains=group_name))
        context = {
            'results': results
        }
        return render(request, 'search_result.html', context)


@is_member_of_group
@not_suspended_member
def comment_on_post(request, group_pk, post_pk):
    post = Post.objects.get(group__pk=group_pk, pk=post_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data.get("content")
            comment = Comment.objects.create(
                member=request.user, content=content, post=post, group=Group.objects.get(pk=group_pk))
            comment.save()
        else:
            comment_form = CommentForm(request.POST)
            messages.error(request, "Comment Creation Failed")
            return render(request, 'comment.html', {
                "comment_form": comment_form,
            })


@is_member_of_group
@not_suspended_member
@login_required(login_url="login")
def reply_comment(request, group_pk, post_pk, comment_pk):
    comment = Comment.objects.get(
        group__pk=group_pk, post__pk=post_pk, pk=comment_pk)
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            content = reply_form.cleaned_data.get("content")
            Replies.objects.create(member=request.user,
                                   content=content, group=Group.objects.get(pk=group_pk), comment=comment)


@login_required(login_url="login")
# @is_member_of_group
# @not_suspended_member
def like_post(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    group_member = group.group_member.all().filter(member=request.user)
    if group_member.is_suspended is False:
        post = Post.objects.filter(pk=post_pk)
        if request.user not in post.like.all():
            post.like.add(request.user)
            liked = True
            notification = Notification.object.create(notification_type="like")
        else:
            post.like.add(request.user)
            liked = Falsecomment = Comment.objects.filter(post__pk=post_pk)
    #     reply = Replies.objects.filter(comment__pk=comment.pk)
    #     liked = Like.objects.filter(member=request.user, post=post)
    #     if not liked:
    #         pass
    # else:
    #     return JsonResponse({"message": "Permission Denied",
    #                          })

    #     comment = Comment.objects.filter(post__pk=post_pk)
    #     reply = Replies.objects.filter(comment__pk=comment.pk)
    #     liked = Like.objects.filter(member=request.user, post=post)
    #     if not liked:
    #         pass
    # else:
    #     return JsonResponse({"message": "Permission Denied",
    #                          })


def like_comment(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    group_member = group.group_member.all().filter(member=request.user)
    if group_member.is_suspended is False:
        post = Post.objects.filter(pk=post_pk)
        comment = Comment.objects.filter(post__pk=post_pk)
        reply = Replies.objects.filter(comment__pk=comment.pk)
        liked = Like.objects.filter(member=request.user, post=post)
        if not liked:
            pass
    else:
        return JsonResponse({"message": "Permission Denied",
                             })


def like_reply(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    group_member = group.group_member.all().filter(member=request.user)
    if group_member.is_suspended is False:
        post = Post.objects.filter(pk=post_pk)
        comment = Comment.objects.filter(post__pk=post_pk)
        reply = Replies.objects.filter(comment__pk=comment.pk)
        liked = Like.objects.filter(member=request.user, post=post)
        if not liked:
            pass
    else:
        return JsonResponse({"message": "Permission Denied",
                             })
