
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from groups.models import Group, Member
from notification.forms import EventForm
from notification.models import Notification, Event

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from groups.models import Group

from .models import Event, Notification
from .forms import EventForm
from poll.models import Poll


logger = logging.getLogger(__name__)
# Create your views here.
print(logger, 'here')


def show_notification(request):
    notify = Notification.objects.filter(
        receiver=request.user, is_seen=False).order_by("-time_created")
    return render(request, "groups/group_detail.html", {
        "notification": notify
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
    notifications_qs = Notification.objects.all()
    # filter(
    #     receiver=request.user).order_by("-time_created")
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


def create_event(request, group_pk):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')

            group = Group.objects.get(group_pk=group_pk)

            Event.objects.create(creator=request.user, group=group, title=title, description=description,
                                 start_time=start_time,
                                 end_time=end_time)
            return redirect('event-list')


def edit_event(request, pk):
    event = Event.objects.get(pk=pk)
    event_form = EventForm(instance=event)

    if request.method == 'POST':
        e_form = EventForm(request.POST, instance=event)

        if e_form.is_valid():
            e_form.save()
            return redirect('event-list')

    context = {
        'event_form': event_form
    }
    return render(request, 'notification/edit-poll.html', context)


def event_list(request):
    events = Event.objects.all().order_by('-date_created')
    context = {
        'events': events
    }
    return render(request, 'notification/event-list.html', context)


def event_on_calender_view(request):
    pass


def create_poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('poll-list')


def edit_poll(request, pk):
    poll = Poll.objects.get(pk=pk)
    pol_form = PollForm(instance=poll)

    if request.method == 'POST':
        poll_form = PollForm(request.POST, instance=poll)

        if poll_form.is_valid():
            poll_form.save()
            return redirect('poll-list')
    context = {
        'poll': poll,
        'pol_form': pol_form
    }
    return render(request, 'notification/poll-detail.html', context)


def vote(request, pk):
    poll = Poll.objects.get(pk=pk)
    member = Member.objects.get(pk=request.user.id)

    if not member.is_suspended:
        try:
            selected_choice = poll.choice_set.get(pk=request.POST)
        except (KeyError, poll.DoesNotExist):
            return render(request, 'notification/detail.html', {
                "poll": poll,
                "error_message": "You didn't select a choice."
            })
        else:
            selected_choice.vote += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('detail', args=[pk]))
