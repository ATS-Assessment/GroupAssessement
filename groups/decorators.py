from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .models import Group


def not_suspended_member(view_func):
    def wrapper_func(request, *args, **kwargs):
        group_pk = kwargs["group_pk"]
        group = Group.objects.get(pk=group_pk)
        group_member = group.group_member.all().filter(member=request.user)
        if group_member.is_suspended is False:
            return view_func(request, *args, **kwargs)
        else:
            return PermissionDenied
    return wrapper_func


def is_member_of_group(view_func):
    def wrapper_func(request, *args, **kwargs):
        group_pk = kwargs["group_pk"]
        group = Group.objects.get(pk=group_pk)
        if request.user in group.group_member.all():
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper_func


# def is_group_admin(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         # group_pk = kwargs[""]
#         group = Group.objects.get(pk=group_pk)
#         members = list(group.group_member.all())
#         if request.user in members and:
#             return view_func(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     return wrapper_func
