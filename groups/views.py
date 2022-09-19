from groups.decorators import is_member_of_group, not_suspended_member
from .models import Group, Member, Post, Member, Like, Replies, GroupRequest, Comment
import json
from django.core.serializers import serialize
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
from django.utils import timezone
from .models import Group
from .forms import CommentForm, GroupForm, PostForm, ReplyForm
from notification.models import Notification


# Create your views here.


<<<<<<< HEAD
@ login_required(login_url='login')
=======
class GroupList(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_list.html"
    context_object_name = "group_list"

    def get_context_data(self, **kwargs):
        context = super(GroupList, self).get_context_data()
        context['member'] = Member.objects.filter(member=self.request.user)
        return context


>>>>>>> origin
def group_list(request):
    groups = Group.objects.all()
    for group in groups:
        members = list(group.group_member.all())
        if group.group_member.filter(member=request.user).exists():
            member = group.group_member.get(member=request.user)
            print(member)

    return render(request, "groups/group_list.html",  {
        "group_list": groups,
        "members": members,
        "member": member,

    })


# class GroupDetail(LoginRequiredMixin, DetailView):
#     model = Group
#     template_name = "groups/group_detail.html"
#     context_object_name = "group"


@ login_required(login_url='login')
@ is_member_of_group
def group_detail(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    group_posts = Post.visible_objects.filter(
        group__pk=group_pk).order_by('-date_created')
    # member = Member.objects.get(pk=request.user.pk)
    member = group.group_member.get(member__pk=request.user.pk)

    if request.method == "POST":

<<<<<<< HEAD
=======

        member = group.group_member.get(member__pk=request.user.pk)

>>>>>>> origin
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            title = post_form.cleaned_data.get("title")
            content = post_form.cleaned_data.get("content")
            post_image = post_form.cleaned_data.get("post_image")
            post_files = post_form.cleaned_data.get("post_files")
            post = Post.objects.create(
                title=title, content=content, post_image=post_image, post_files=post_files, group=group, member=member)
            post.save()
            return redirect(reverse('group-detail', args=[group_pk]))
        else:
            post_form = PostForm()
    else:
        post_form = PostForm()
<<<<<<< HEAD

    contents = Post.objects.all()
    already_liked = []
    id = member.id
    for content in group_posts:
        if (content.like.filter(id=id).exists()):
            already_liked.append(content.id)
    ctx = {"contents": contents, "already_liked": already_liked}

=======
        member = group.group_member.get(member__pk=request.user.pk)
>>>>>>> origin
    context = {
        "current_user": Member.objects.get(member=request.user, group_id=group_pk),
        "group": group,
        "members": group.group_member.all(),
        "count": group.group_member.all().count(),
        "member": member,
        "post_form": post_form,
        "group_post": group_posts,
<<<<<<< HEAD
        "contents": contents,
        "already_liked": already_liked

=======
        "today": timezone.now().date(),
>>>>>>> origin
    }

    # print(group_posts)
    # print(group.group_member.all())
    # (group_posts)
    # print(group.group_member.all())

    for post in group_posts:
        post_comments = Comment.objects.filter(
            post__pk=post.pk, is_hidden=True).order_by('-date_created')

        for comment in post_comments:
            comment_replies = Replies.objects.filter(
                comment__pk=comment.pk).order_by('-date_created')
            context["post_comments"] = post_comments
            context["comment_replies"] = comment_replies
            context["post"] = post
    return render(request, "groups/group_detail.html", context)


<<<<<<< HEAD
@login_required(login_url="login")
@is_member_of_group
@not_suspended_member
def like_post(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    group_member = group.group_member.get(member=request.user)
    if request.method == "POST":
        content_id = request.POST.get("content_id", None)

        if group_member.is_suspended is False:

            post = Post.objects.get(pk=content_id)

            if request.user not in post.like.all():
                post.like.add(group_member)
                liked = True
                notification = Notification.objects.create(
                    notification_type="Like", content_preview="A Member a liked a Post", receiver=request.user)
                # return JsonResponse({
                #     "liked": liked,
                #     "content_id": content_id,
                # })
            else:
                post.like.remove(group_member)
                liked = False
                notification = Notification.object.create(
                    notification_type="Like", content_preview="A Member a unliked a Post", receiver=request.user)
                return JsonResponse({
                    "liked": liked,
                    "content_id": content_id,
                })

    contents = Post.objects.all()
    already_liked = []
    id = group_member.id
    for content in contents:
        if (content.like.filter(id=id).exists()):
            already_liked.append(content.id)
    ctx = {"contents": contents, "already_liked": already_liked}
    return render(request, "groups/group_detail.html", ctx)


@ login_required(login_url='login')
=======
@login_required(login_url='login')
>>>>>>> origin
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


@require_POST
@login_required(login_url="login")
def make_admin(request, group_pk, admin_pk, user_pk):
<<<<<<< HEAD
    group = Group.objects.filter(
        pk=group_pk, creator__pk=admin_pk).first()
    if group.group_member.all().filter(is_admin=True).count() < 3:
        try:
            member = group.group_member.get(member__pk=user_pk)
        except Exception as e:
            print("An error occurred while querying the group member", e)

        member.is_admin = True
        member.save()
        messages.success(
            request, f"{member.user.first_name} has successfully been made an Admin!")
        return redirect(request.META["HTTP_REFERER"])
=======
    if Member.objects.get(member=request.user, group_id=group_pk).is_admin:
        group = Group.objects.get(
            pk=group_pk, creator_id=admin_pk)
        if group.group_member.all().filter(is_admin=True).count() < 3:
            member = group.group_member.get(member_id=user_pk)
            # member = Member.objects.get(member_id=user_pk, group=group)
            member.is_admin = True
            member.save()
            messages.success(
                request, f"{member.member.first_name} has successfully been made an Admin!")
            return redirect('group-detail', group.id)
        else:
            messages.error(
                request, "Group Admins cannot be more than 3!")
            return redirect('group-detail', group.id)

>>>>>>> origin
    else:
        messages.error(request, "Only admin can make member an admin.")
        return redirect('group-detail', group_pk)


@require_POST
@login_required(login_url='login')
def remove_group_member(request, group_pk, admin_pk, user_pk):
    if Member.objects.get(member=request.user, group_id=group_pk).is_admin:
        group = Group.objects.get(
            pk=group_pk, creator_id=admin_pk)
        member = group.group_member.get(member_id=user_pk)
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
    group_request = GroupRequest.objects.create(
        user=request.user, group=group)
    # admins = group.group_member.all().filter(member__is_admin=True)
    # for admin in admins:
    Notification.objects.create(group=group,
<<<<<<< HEAD
                                notification_type="Group Request", content_preview="A Potential Member wants to join your Group", is_admin_notification=True)
=======
                                notification_type="group_request",
                                content_preview="A Potential Member wants to join your Group",
                                is_admin_notification=True)
>>>>>>> origin
    return redirect(request.META["HTTP_REFERER"])


def request_add(request, group_pk, user_pk):
    group = Group.objects.get(pk=group_pk)
    user = User.objects.get(pk=user_pk)
    new_member = Member.objects.create(
        group=group, member=user)
    return redirect(reverse('group-detail', args=[group_pk]))


def join_group(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    if not Member.objects.filter(member=request.user).exists():
        Member.objects.create(group=group, member=request.user)
        return redirect(reverse("group-detail", args=[group_pk]))
    return redirect(request.META.get("HTTP_REFERER"))


def request_reject_():
    pass


@login_required(login_url="login")
def accept_to_group(request):
    member = request.user.user_member
    if member.is_admin:
        pass


@require_POST
@login_required(login_url='login')
def exit_group(request, group_name, user_pk):
    group = Group.objects.get(name=group_name)
    member = group.group_member.filter(user__pk=user_pk)
    member.has_exited = True
    member.save()
    member.save()
    messages.success(
        request, f"{member.user.first_name} has successfully exited from the Group!")
    return redirect("group-list")


def suspend_member(request, group_pk, admin_pk, user_pk):
    if Member.objects.get(member=request.user, group_id=group_pk).is_admin:
        group = Group.objects.get(pk=group_pk, creator_id=admin_pk)
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
        print(group_name)
        results = Group.objects.filter(
            Q(name__icontains=group_name) | Q
            (description__icontains=group_name))
        context = {
            'results': results
        }
        return render(request, 'search.html', context)


# @is_member_of_group
# @not_suspended_member
def comment_on_post(request, group_pk, post_pk):
    post = Post.objects.get(group__pk=group_pk, pk=post_pk)
<<<<<<< HEAD

=======
    group = Group.objects.get(pk=group_pk)
>>>>>>> origin
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        # comment = request.GET.get('content', None)
        if comment_form.is_valid():
            content = comment_form.cleaned_data.get("content")
            comment = Comment.objects.create(
                member=group.group_member.get(member=request.user), content=content, post=post, group=group)
            comment.save()
<<<<<<< HEAD
            data = {
                "comment": comment
            }
            return JsonResponse(comment)
=======
            return redirect('group-detail', group.id)
>>>>>>> origin
        else:
            comment_form = CommentForm(request.POST)
            messages.error(request, "Comment Creation Failed")
            return redirect('group-detail', group.id)
    else:
        comment_form = CommentForm()
        return render(request, 'groups/group_detail.html', {
            "comment_form": comment_form,
        })


# @is_member_of_group
# @not_suspended_member
@login_required(login_url="login")
def reply_comment(request, group_pk, post_pk, comment_pk):
    group = Group.objects.get(pk=group_pk)

    member = group.group_member.get(member__pk=request.user.pk)
    comment = Comment.objects.get(
        group__pk=group_pk, post__pk=post_pk, pk=comment_pk)
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            content = reply_form.cleaned_data.get("content")
            if member:
                new_reply = Replies.objects.create(member=member,
                                                   content=content, comment=comment)
                print("ok")
                print(new_reply.member.member.first_name)
                print(new_reply.member.member.last_name)
                resp = {
                    "content": new_reply.content,
                    "first_name": new_reply.member.member.first_name,
                    "last_name": new_reply.member.member.last_name,

                }
                print("noe")
                return JsonResponse(resp, content_type="application/json")
        else:
            print(reply_form.errors)
            return JsonResponse({"Error": reply_form.errors}, content_type="application/json")
    else:
        return JsonResponse({
            "message": "Not Allowed"
        })


@login_required(login_url="login")
@is_member_of_group
@not_suspended_member
def like_post(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    group_member = group.group_member.get(member=request.user)
    if request.method == "POST":
        content_id = request.POST.get("content_id", None)

        if group_member.is_suspended is False:

            post = Post.objects.get(pk=content_id)

            if request.user not in post.like.all():
                post.like.add(group_member)
                liked = True
                notification = Notification.objects.create(
<<<<<<< HEAD
                    notification_type="Like", content_preview="A Member a liked a Post", receiver=request.user)
                # return JsonResponse({
                #     "liked": liked,
                #     "content_id": content_id,
                # })
=======
                    notification_type="like", content_preview="A Member liked a Post", receiver=request.user)
                return JsonResponse({
                    "liked": liked,
                    "content_id": content_id,
                })
>>>>>>> origin
            else:
                post.like.remove(group_member)
                liked = False
                notification = Notification.object.create(
<<<<<<< HEAD
                    notification_type="Like", content_preview="A Member a unliked a Post", receiver=request.user)
=======
                    notification_type="like", content_preview="A Member unliked a Post", receiver=request.user)
>>>>>>> origin
                return JsonResponse({
                    "liked": liked,
                    "content_id": content_id,
                })

    contents = Post.objects.all()
    already_liked = []
    id = group_member.id
    for content in contents:
        if (content.like.filter(id=id).exists()):
            already_liked.append(content.id)
    ctx = {"contents": contents, "already_liked": already_liked}
    return render(request, "groups/group_detail.html", ctx)


# def like_button(request):
#     if request.method == "POST":
#         if request.POST.get("operation") == "like_submit":
#             content_id = request.POST.get("content_id", None)
#             content = get_object_or_404(LikeButton, pk=content_id)
#             # already liked the content
#             if content.likes.filter(id=request.user.id):
#                 content.likes.remove(request.user)  # remove user from likes
#                 liked = False
#             else:
#                 content.likes.add(request.user)
#                 liked = True
#             ctx = {"likes_count": content.total_likes,
#                    "liked": liked, "content_id": content_id}
#             return HttpResponse(json.dumps(ctx), content_type='application/json')

#     contents = LikeButton.objects.all()
#     already_liked = []
#     id = request.user.id
#     for content in contents:
#         if (content.likes.filter(id=id).exists()):
#             already_liked.append(content.id)
#     ctx = {"contents": contents, "already_liked": already_liked}
#     return render(request, "like/like_template.html", ctx)


def like_comment(request, group_pk, post_pk, comment_pk):
    group = Group.objects.get(pk=group_pk)
    group_member = group.group_member.all().filter(member=request.user)
    group_member = group.group_member.get(member=request.user)
    print(group_member)
    if group_member.is_suspended is False:
        comment = Comment.objects.get(pk=comment_pk, post__pk=post_pk)
        # reply = Replies.objects.filter(comment__pk=comment.pk)
        liked = Like.objects.filter(
            member=request.user, post__pk=post_pk, comment__pk=comment_pk)
        print(liked)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        # if not liked:
        #     pass
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


def hide_post(request, group_pk, post_pk):
    group = Group.objects.get(pk=group_pk)
    print("HidePost")
    group_member = group.group_member.all().filter(member=request.user)
    if group_member.is_admin:
        post = Post.objects.filter(pk=post_pk)
        post.is_hidden = True

        return JsonResponse({
            "hidden": post.is_hidden,
            "post_pk": post.pk,
        })


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
