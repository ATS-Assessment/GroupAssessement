from poll.models import Poll
from .models import Notification
from groups.models import Group
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from notification.models import Notification
from groups.models import Group, Member
import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from event.models import Event
<<<<<<< HEAD
from groups.models import Group, Member
from notification.models import Notification
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from groups.models import Group
from .models import Notification
from poll.models import Poll
=======
>>>>>>> refs/remotes/origin/main

logger = logging.getLogger(__name__)
# Create your views here.
print(logger, 'here')


def show_notification(request, event_pk):
    member = Member.objects.get(member__pk=request.user.pk)
    event = Event.objects.get(pk=event_pk)
    notify = Notification.objects.filter(
        receiver=request.user, is_seen=False).order_by("-time_created")
    return render(request, "groups/group_detail.html", {
        "notification": notify,
        "member": member,
        "event": event,

    })


# @login_required(login_url='login')
# def count_notification(request):
#     if not request.user.pk:
#         return {}
#     noti_count = Notification.objects.filter(
#         receiver=request.user, is_seen=False).count()
#     return {
#         "noti_count": noti_count,
#         "e": 2
#     }


@login_required
def notification_list(request):
    logger.debug("notification_list called by user %s" % request.user)
    # event = Event.objects.get(pk=event_pk)
    notifications_qs = Notification.objects.all()

    # filter(
    #     receiver=request.user).order_by("-time_created")

    # member = Member.objects.get(member__pk=request.user.pk)
    new_notifs = notifications_qs.filter(is_seen=False)
    old_notifs = notifications_qs.filter(is_seen=True)
    logger.debug(
        "User %s has %s unread and %s read notifications",
        request.user,
        len(new_notifs),
        len(old_notifs)
    )
    context = {
        "notifications_qs": notifications_qs,
        'read': old_notifs,
        'unread': new_notifs,
        # "member": member,
        # "event": event,
    }
    return render(request, 'notification.html', context)


@login_required
def notification_view(request, notif_pk):
    logger.debug(
        "notification_view called by user %s for notif_id %s",
        request.user,
        notif_pk
    )
    notif = get_object_or_404(Notification, pk=notif_pk)
    if notif.receiver == request.user:
        logger.debug("Providing notification for user %s", request.user)
        context = {'notif': notif}
        notif.mark_as_seen()
        return render(request, 'notifications/view.html', context)
    else:
        logger.warn(
            "User %s not authorized to view notif_id %s belonging to user %s",
            request.user,
            notif_pk, notif.user
        )
        messages.error(request, _(
            'You are not authorized to view that notification.'))
        return redirect('notification-list')


@login_required
def remove_notification(request, notif_pk):
    logger.debug(
        "remove notification called by user %s for notif_id %s",
        request.user,
        notif_pk
    )
    notif = get_object_or_404(Notification, pk=notif_pk)
    if notif.receiver == request.user:
        if Notification.objects.filter(id=notif_pk).exists():
            notif.delete()
            logger.info("Deleting notif id %s by user %s",
                        notif_pk, request.user)
            messages.success(request, _('Deleted notification.'))
            return redirect('notification-list')
    else:
        logger.error(
            "Unable to delete notif id %s for user %s - notif matching id not found.",
            notif_pk,
            request.user
        )
        messages.error(request, _('Failed to locate notification.'))
    return redirect('notification-list')


@login_required
def mark_all_read(request):
    logger.debug('mark all notifications read called by user %s', request.user)
    Notification.objects.filter(receiver=request.user).update(is_seen=True)
    messages.success(request, _('Marked all notifications as read.'))
    return redirect('notification-list')


@login_required
def delete_all_read(request):
    logger.debug(
        'delete all read notifications called by user %s', request.user)
    Notification.objects.filter(
        receiver=request.user).filter(is_seen=True).delete()
    messages.success(request, _('Deleted all read notifications.'))
    return redirect('notification-list')


# def user_notifications_count(request, user_pk: int):
#     """returns to notifications count for the give user as JSON
#     This view is public and does not require login
#     """
#     unread_count = Notification.objects.user_unread_count(user_pk)
#     data = {'unread_count': unread_count}
#     return JsonResponse(data, safe=False)


def count_notification(request):
    if not request.user.pk:
        return {}
    noti_count = Notification.objects.filter(
        receiver=request.user, is_seen=False).count()
    return dict(noti_count=noti_count)


def event_on_calender_view(request):
    pass
