from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notification.models import Notification

# Create your views here.


def show_notification(request):
    notify = Notification.objects.filter(
        receiver=request.user, is_viewed=False).order_by("-date_created")
    return render(request, "groups/group_detail.html", {
        "notification": notify
    })


@login_required(login_url='login')
def count_notification(request):
    noti_count = Notification.objects.filter(
        receiver=request.user, is_viewed=False).count()
    return dict(noti_count=noti_count)
