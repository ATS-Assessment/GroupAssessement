
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Event, Notification
from .forms import EventForm

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
        receiver=request.user, is_seen=False).count()
    return dict(noti_count=noti_count)


def create_event(request):

    if request.method == "POST":
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            title = event_form.cleaned_data.get('title')
            description = event_form.cleaned_data.get('description')

            event_form.save()
            return redirect()


def view_events(request):
    event = Event.objects.all()
    return render(request, "events/event_list.html", {
        "events": event
    })


def edit_event(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    if request.method == "POST":
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect(reverse('edit-event', args=[event_pk]))
