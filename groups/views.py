

from .models import Group, Member, Post, Member, Like, Replies, GroupRequest
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Group
from .forms import GroupForm

# Create your views here.


class GroupList(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_list.html"
    context_object_name = "group_list"


# class GroupDetail(LoginRequiredMixin, DetailView):
#     model = Group
#     template_name = "groups/group_detail.html"
#     context_object_name = "group"

def group_detail(request, group_pk):
    group = Group.objects.get(pk=group_pk)

    return render(request, "groups/group_detail.html", {
        "group": group,
        "members": group.group_member.all(),
        "count": group.group_member.all().count(),
        "member": Member.objects.all(),
    })


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
                name=name,
                description=description,
                privacy_status=privacy_status,
                creator=request.user,
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
def make_admin(request, group_name, admin_pk, user_pk):
    group = Group.objects.filter(
        name=group_name, creator__pk=admin_pk).first()
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
def remove_group_member(request, group_name, admin_pk, user_pk):
    group = Group.objects.filter(
        name=group_name, creator__pk=admin_pk)
    member = group.group_member.filter(user__pk=user_pk)
    member.has_exited = True
    member.save()
    messages.success(
        request, f"{member.user.first_name} has successfully been removed from the Group!")
    return redirect(request.META["HTTP_REFERER"])


# @require_POST
# @login_required(login_url='login')
# def join_group(request, pk):
#     group = Group.objects.get(id=pk)
#     members = group.group_member.all()
#     if request.user not in members:
#         new_member = Member.objects.create(group=group, member=request.user, is_admin=False)
#     else:
#         group.group_member.objects.remove(group=group, member=request.user)
#     group.save()
#     new_member.save()
#     return render(request, 'groups/group_list.html', {'new_member': new_member, 'members': members})


@login_required(login_url='login')
def request_to_join_group(request, group_name, user_pk):
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


def suspend_member(request, group_name, admin_pk, user_pk):
    group = Group.objects.get(name=group_name, user__pk=admin_pk).first()
    member = group.group_member.filter(user__pk=user_pk)
    member.is_suspended = True
    member.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url='login')
def create_post(request, group_pk):
    group = Group.objects.get(pk=group_pk)
    group_member = group.group_member.all().filter(member=request.user)
    if group_member.is_suspended is False:
        post = Post.objects.create(
            title="", content="", group=group, member=request.user)
        post.save()
        return JsonResponse({"data": post})
    else:
        return JsonResponse({"message": "Permission Denied",
                             })
