from django.shortcuts import render
from .models import Notification
# @login_required(login_url='login')


def count_notification(request):
    if not request.user.pk:
        return {"noti_count": 0}
    if request.user.is_authenticated:
        noti_count = Notification.objects.filter(
            receiver=request.user, is_seen=False).count()
        return {
            "noti_count": noti_count
        }
