
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from groups.models import Group

from .models import Event, Notification
from .forms import EventForm

# Create your views here.


def show_notification(request):
    notify = Notification.objects.filter(
        receiver=request.user, is_viewed=False).order_by("-date_created")
    return render(request, "groups/group_detail.html", {
        "notification": notify
    })


# @login_required(login_url='login')
def count_notification(request):
    if not request.user.pk:
        return {}
    noti_count = Notification.objects.filter(
        receiver=request.user, is_seen=False).count()
    return dict(noti_count=noti_count)

# def count_notification(request):
#     if not request.user.pk:
#         return {}
#     noti_count = Notification.objects.filter(
#         receiver=request.user, is_seen=False).count()
#     return {
#         "noti_count": noti_count,
#         "e": 2
#     }
