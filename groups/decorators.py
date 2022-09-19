from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .models import Group, Member


def not_suspended_member(view_func):
    def wrapper_func(request, *args, **kwargs):
        group_pk = kwargs.pop("group_pk", None)
        group = Group.objects.get(pk=group_pk)
        member = Member.objects.get(pk=request.user.pk)
        group_member = group.group_member.all().filter(member=request.user)
        if group_member.is_suspended is False:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(
                request, "You cant access this group cause you are not a member of this group!")
            return PermissionDenied
    return wrapper_func


def is_member_of_group(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            group_pk = int(kwargs.get('group_pk', None))
            group = Group.objects.get(pk=group_pk)
            member = Member.objects.get(
                member__pk=request.user.pk, group=group)
            if member in group.group_member.all():
                return view_func(request, *args, **kwargs)
        except (Member.DoesNotExist) as e:
            messages.error(
                request, e, "You cant access this group cause you are not a member of this group!")
            raise PermissionDenied
    return wrapper_func


def is_group_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        group_pk = kwargs.pop("group_pk", None)
        group = Group.objects.get(pk=group_pk)
        member = Member.objects.get(pk=request.user.pk, group=group)
        members = list(group.group_member.all())
        if members in members and member.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(
                request, "You cant access this group cause you are not a member or an Admin of this group!")
            raise PermissionDenied
    return wrapper_func
