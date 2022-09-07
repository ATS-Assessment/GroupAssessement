from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from groups.models import Group
from notification.forms import EventForm
from notification.models import Notification, Event


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
