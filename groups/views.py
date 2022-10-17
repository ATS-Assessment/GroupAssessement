from groups.decorators import is_member_of_group, not_suspended_member
from .models import Group, Member, Post, Member, Like, Replies, GroupRequest, Comment
import json
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from account.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone

from notifications.signals import notify

from .models import Group
from .forms import CommentForm, GroupForm, PostForm, ReplyForm
from notification.models import Notification


# Create your views here.


class GroupList(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_list.html"
    context_object_name = "group_list"


@login_required(login_url='login')
@is_member_of_group
def group_detail(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    group_posts = Post.visible_objects.filter(
        group__pk=group_pk).order_by('-date_created')

    if request.method == "POST":

        member = group.group_member.get(member__pk=request.user.pk)

        if not member.is_suspended:

            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                title = post_form.cleaned_data.get("title")
                content = post_form.cleaned_data.get("content")
                post_image = post_form.cleaned_data.get("post_image")
                post_files = post_form.cleaned_data.get("post_files")
                Post.objects.create(
                    title=title, content=content, post_image=post_image, post_files=post_files, group=group,
                    member=member)
                admins = group.group_member.filter(is_admin=True)
                admin_list = []
                for admin in admins:
                    admin_list.append(admin.member)
                notify.send(sender=member, recipient=admin_list, verb=f"{member} create a post",
                            description="Post create")
                return redirect(reverse('group-detail', args=[group_pk]))
            else:
                post_form = PostForm()
        else:
            messages.error(request, "Suspended member cannot post.")
            return redirect('group-detail', group.id)
    else:
        post_form = PostForm()
        member = group.group_member.get(member__pk=request.user.pk)

    if not group.group_member.get(member=request.user).is_admin:
        context = {
            "current_member": Member.objects.get(member=request.user, group_id=group_pk),
            "group": group,
            "members": group.group_member.all(),
            "count": group.group_member.all().count(),
            "member": member,
            "post_form": post_form,
            "group_post": group_posts,
            "today": timezone.now().date(),
            "admin": Member.objects.filter(group_id=group_pk).filter(is_admin=True).count(),
        }
    else:
        context = {
            "current_member": Member.objects.get(member=request.user, group_id=group_pk),
            "group": group,
            "members": group.group_member.all(),
            "count": group.group_member.all().count(),
            "member": member,
            "post_form": post_form,
            "group_post": Post.objects.filter(group__pk=group_pk).order_by('-date_created'),
            "today": timezone.now().date(),
            "admin": Member.objects.filter(group_id=group_pk).filter(is_admin=True).count(),
        }

    return render(request, "groups/group_detail.html", context)


@login_required(login_url='login')
def create_group(request):
    if request.method == "POST":
        group_form = GroupForm(request.POST, request.FILES)
        if group_form.is_valid():
            name = group_form.cleaned_data.get("name")
            description = group_form.cleaned_data.get("description")
            privacy_status = group_form.cleaned_data.get("privacy_status")
            group_image = group_form.cleaned_data.get("group_image")
            group = Group.objects.create(
                name=name, description=description, privacy_status=privacy_status, creator=request.user,
                group_image=group_image)
            new_member = Member.objects.create(
                group=group, member=group.creator, is_admin=True)
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


@require_POST
@login_required(login_url="login")
def make_admin(request, group_pk, user_pk):
    if Member.objects.get(member=request.user, group_id=group_pk).is_admin:
        group = Group.objects.get(
            pk=group_pk)
        if not group.group_member.get(member_id=user_pk).is_suspended:
            if group.group_member.all().filter(is_admin=True).count() < 3:
                member = group.group_member.get(member_id=user_pk)
                # member = Member.objects.get(member_id=user_pk, group=group)
                if group.creator.id == member.member.id:
                    messages.error(request, "You can't remove creator from admin")
                member.is_admin = not member.is_admin
                member.save()
                messages.success(
                    request, f"{member.member.first_name} has successfully been made an Admin!")
                return redirect('group-detail', group.id)
            else:
                messages.error(
                    request, "Group Admins cannot be more than 3!")
                return redirect('group-detail', group.id)
        else:
            messages.error(
                request, "Suspended member cannot be admin")
            return redirect('group-detail', group.id)
    else:
        messages.error(request, "Only admin can make member an admin.")
        return redirect('group-detail', group_pk)


@require_POST
@login_required(login_url='login')
def remove_group_member(request, group_pk, admin_pk, user_pk):
    if Member.objects.get(member=request.user, group_id=group_pk).is_admin:
        group = Group.objects.get(
            pk=group_pk)
        member = group.group_member.get(member_id=user_pk)
        if group.creator.id == member.member.id:
            messages.error(request, "You can't remove creator.")
            return redirect('group-detail', group.id)
        member.delete()
        messages.success(
            request, f"{member.member.first_name} has successfully been removed from the Group!")
        return redirect('group-detail', group.id)
    else:
        messages.error(request, "Only admin can remove member of a group")
        return redirect('group-detail', group_pk)


@login_required(login_url='login')
def request_to_join_group(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    notify.send(sender=request.user, recipient=group.creator, action_object=group,
                verb=f"{request.user} request to join group", description="Join request")
    return redirect('group-list')


def request_add(request, group_pk, user_pk):
    group = Group.objects.get(pk=group_pk)
    user = User.objects.get(pk=user_pk)
    Member.objects.create(
        group=group, member=user)
    return redirect('group-detail', group.id)


def join_group(request, group_pk, user_pk):
    group = Group.objects.get(pk=group_pk)
    if not Member.objects.filter(member_id=user_pk, group=group).exists():
        Member.objects.create(group=group, member_id=user_pk)
        return redirect('group-detail', group.id)
    return redirect('group-list')


def request_reject_():
    pass


@login_required(login_url="login")
def accept_to_group(request):
    member = request.user.user_member
    if member.is_admin:
        pass


@require_POST
@login_required(login_url='login')
def exit_group(request, group_pk, user_pk):
    group = get_object_or_404(Group, pk=group_pk)
    member = group.group_member.get(member_id=user_pk)
    member.delete()
    messages.success(
        request, f"{member.member.first_name} has successfully exited from the Group!")
    return redirect("group-list")


def suspend_member(request, group_pk, user_pk):
    if Member.objects.get(member=request.user, group_id=group_pk).is_admin:
        group = Group.objects.get(pk=group_pk)
        member = group.group_member.get(member_id=user_pk)
        member.is_suspended = not member.is_suspended
        member.save()
        return redirect('group-detail', group.id)
    else:
        messages.error(request, "Only admin can suspend a member")
        return redirect("group-detail", group_pk)


@login_required(login_url="login")
def search_groups(request):
    if request.method == "GET" and "keyword" in request.GET:
        group_name = request.GET.get('keyword')
        results = Group.objects.filter(
            Q(name__icontains=group_name) | Q
            (description__icontains=group_name))
        context = {
            'results': results
        }
        return render(request, 'search.html', context)


def comment_on_post(request, group_pk, post_pk):
    post = Post.objects.get(group__pk=group_pk, pk=post_pk)
    group = Group.objects.get(pk=group_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        member = group.group_member.get(member=request.user)
        if not member.is_suspended:
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get("content")
                comment = Comment.objects.create(
                    member=member, content=content, post=post, group=group)
                admins = group.group_member.filter(is_admin=True)
                admin_list = []
                for admin in admins:
                    admin_list.append(admin.member)
                notify.send(member, recipient=admin_list, verb=f"{member.member.first_name} comment",
                            description=f"{member.member.first_name} comment on a post")
                return redirect('group-detail', group.id)
            else:
                comment_form = CommentForm(request.POST)
                messages.error(request, "Comment Creation Failed")
                return redirect('group-detail', group.id)
        else:
            messages.error(request, "Suspended member cannot comment.")
            return redirect('group-detail', group.id)
    else:
        comment_form = CommentForm()
        return render(request, 'groups/group_detail.html', {
            "comment_form": comment_form,
        })


@login_required(login_url="login")
def reply_comment(request, group_pk, post_pk, comment_pk):
    group = Group.objects.get(pk=group_pk)

    member = group.group_member.get(member__pk=request.user.pk)
    comment = Comment.objects.get(
        group__pk=group_pk, post__pk=post_pk, pk=comment_pk)
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if not member.is_suspended:
            if reply_form.is_valid():
                content = reply_form.cleaned_data.get("content")
                if member:
                    new_reply = Replies.objects.create(member=member,
                                                       content=content, comment=comment)

                    admins = group.group_member.filter(is_admin=True)
                    admin_list = []
                    for admin in admins:
                        admin_list.append(admin.member)
                    notify.send(sender=member, recipient=admin_list, verb=f"{member.member.first_name} reply comment",
                                description=f"{member.member.first_name} reply on a comment")
                    return redirect('group-detail', group.id)
        else:
            messages.error(request, "Suspended member cannot reply comment.")
            return redirect('group-detail', group.id)

    else:
        replies = Replies.objects.all().order_by("-date_created")
        return render(request, "groups/group_detail.html", {"replies": replies})


def like_post(request, group_pk, post_pk):
    if request.method == "POST":
        group = Group.objects.get(pk=group_pk)
        group_member = group.group_member.get(member=request.user)
        if not group_member.is_suspended:
            post = Post.objects.get(pk=post_pk)
            if group_member not in post.like.all():
                post.like.add(group_member)
                post.save()

                admins = group.group_member.filter(is_admin=True)
                admin_list = []
                for admin in admins:
                    admin_list.append(admin.member)
                notify.send(sender=group_member, recipient=admin_list,
                            verb=f"{group_member.member.first_name} like a post",
                            description=f"{group_member.member.first_name} like a post")
                notify.send(sender=group_member, recipient=post.member.member,
                            verb=f"{group_member} like your post",
                            description=f"{group_member} like your post")

                return redirect('group-detail', group.id)
            else:
                post.like.remove(group_member)
                post.save()
                liked = False
                Notification.objects.create(
                    notification_type="like", content_preview="A Member unliked a Post", receiver=group_member)
                return redirect('group-detail', group.id)
        else:
            messages.error(request, "Suspended member can not like post")
            return redirect('group-detail', group.id)


def like_comment(request, group_pk, post_pk, comment_pk):
    if request.method == 'POST':
        group = Group.objects.get(pk=group_pk)
        group_member = group.group_member.get(member=request.user)
        if not group_member.is_suspended:
            comment = Comment.objects.get(pk=comment_pk, post_id=post_pk)
            if group_member not in comment.like.all():
                comment.like.add(group_member)
                comment.save()
                admins = group.group_member.filter(is_admin=True)
                admin_list = []
                for admin in admins:
                    admin_list.append(admin.member)
                notify.send(sender=group_member, recipient=admin_list,
                            verb=f"{group_member.member.first_name} like a comment",
                            description=f"{group_member.member.first_name} like a comment")
                notify.send(sender=group_member, recipient=comment.member.member,
                            verb=f"{group_member} like your comment",
                            description=f"{group_member} like your comment")
                return redirect('group-detail', group.id)
            else:
                comment.like.remove(group_member)
                comment.save()
            return redirect('group-detail', group.id)

        else:
            messages.error(request, "Suspended member cannot like comment")
            return redirect('group-detail', group.id)


def like_reply(request, group_pk, post_pk, comment_pk, reply_comment_pk):
    if request.method == 'POST':
        group = Group.objects.get(pk=group_pk)
        group_member = group.group_member.get(member=request.user)
        if not group_member.is_suspended:
            comment = Comment.objects.get(pk=comment_pk, post_id=post_pk)
            reply = Replies.objects.get(pk=reply_comment_pk, comment=comment)
            if group_member not in reply.like.all():
                reply.like.add(group_member)
                reply.save()

                admins = group.group_member.filter(is_admin=True)
                admin_list = []
                for admin in admins:
                    admin_list.append(admin.member)
                notify.send(sender=group_member, recipient=admin_list,
                            verb=f"{group_member.member.first_name} like a reply",
                            description=f"{group_member.member.first_name} like a reply")
                notify.send(sender=group_member, recipient=reply.member.member,
                            verb=f"{group_member} like your reply",
                            description=f"{group_member} like your reply")

                return redirect('group-detail', group.id)
            else:
                reply.like.remove(group_member)
                reply.save()
                return redirect('group-detail', group.id)
        else:
            messages.error(request, 'Suspended member cannot like reply')
            return redirect('group-detail', group.id)


def hide_post(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    member = group.group_member.get(member=request.user)
    if member.is_admin:
        post = Post.objects.get(pk=post_pk)
        post.is_hidden = not post.is_hidden
        post.save()

        return redirect('group-detail', group.id)


def hide_comment(request, group_pk, post_pk, comment_pk):
    group = Group.objects.get(pk=group_pk)
    member = group.group_member.get(member=request.user)
    if member.is_admin:
        post = Post.objects.get(pk=post_pk)
        comment = post.post_comment.get(pk=comment_pk)
        comment.is_hidden = not comment.is_hidden
        comment.save()

        return redirect('group-detail', group.id)


def hide_reply_comment(request, group_pk, post_pk, comment_pk, reply_comment_pk):
    group = Group.objects.get(pk=group_pk)
    member = group.group_member.get(member=request.user)
    if member.is_admin:
        post = Post.objects.get(pk=post_pk)
        comment = post.post_comment.get(pk=comment_pk)
        reply_comment = comment.comment_replies.get(pk=reply_comment_pk)
        reply_comment.is_hidden = not reply_comment.is_hidden
        reply_comment.save()

        return redirect('group-detail', group.id)


@login_required(login_url='login')
def dashboard(request):
    return render(request, "groups/dashboard.html")


def page_404(request, exception=None):
    return render(request, "groups/404.html")


def page_403(request, exception=None):
    return render(request, "groups/403.html")


def page_400(request, exception=None):
    return render(request, "groups/404.html")


def page_500(request, exception=None):
    return render(request, "groups/404.html")


def confirmation(request):
    return render(request, "groups/confirmation.html")
