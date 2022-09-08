from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from groups.models import Group, Member
from notification.forms import EventForm, PollForm
from notification.models import Notification, Event, Poll

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
            selected_choice.vote +=1
            selected_choice.save()
            return HttpResponseRedirect(reverse('detail', args=[pk]))
