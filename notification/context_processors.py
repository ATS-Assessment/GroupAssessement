from django.shortcuts import render
from .models import Notification
# @login_required(login_url='login')


def count_notification(request):
    if not request.user.pk:
        return {"noti_count": 0}
    if request.user.is_authenticated:
        noti_count = Notification.objects.all().count()
        notifications_qs = Notification.objects.all()
        return {
            "noti_count": noti_count,
            "noti": notifications_qs,
        }


# @login_required
# def notification_list(request):
#     logger.debug("notification_list called by user %s" % request.user)
#     notifications_qs = Notification.objects.all()
#     # filter(
#     #     receiver=request.user).order_by("-time_created")
#     new_notifs = notifications_qs.filter(is_seen=False)
#     old_notifs = notifications_qs.filter(is_seen=True)
#     logger.debug(
#         "User %s has %s unread and %s read notifications",
#         request.user,
#         len(new_notifs),
#         len(old_notifs)
#     )
#     context = {
#         "notifications_qs": notifications_qs,
#         'read': old_notifs,
#         'unread': new_notifs,
#     }
#     return render(request, 'notification.html', context)
