from __future__ import print_function
from django.views.generic import DeleteView
from django.views.generic.list import BaseListView
from django.urls import reverse
from django.shortcuts import render
import string
import random
import pickle
from django.http.response import HttpResponse
import httplib2
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os.path
import pytz
import datetime
import calendar
from calendar import HTMLCalendar
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView, DetailView
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.contrib import messages
from notification.models import EventInvite, Notification
from django.urls import reverse_lazy, reverse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .forms import EventForm
from .utils import Calendar
from groups.decorators import is_group_admin
from groups.models import Group, Member
from .models import EventMember, Event

SCOPES = ["https://www.googleapis.com/auth/calendar"]
service_account_email = "socialv@django-group.iam.gserviceaccount.com"
credentials = service_account.Credentials.from_service_account_file(
    'api-key.json')
scoped_credentials = credentials.with_scopes(SCOPES)


def build_service(request):
    service = build("calendar", "v3", credentials=scoped_credentials)
    return service


# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#     try:
#         service = build('calendar', 'v3', credentials=creds)
#         # Call the Calendar API
#         now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
#         print('Getting the upcoming 10 events')
#         events_result = service.events().list(calendarId='primary', timeMin=now,
#                                               maxResults=10, singleEvents=True,
#                                               orderBy='startTime').execute()
#         events = events_result.get('items', [])
#         if not events:
#             print('No upcoming events found.')
#             return
#         # Prints the start and name of the next 10 events
#         for event in events:
#             start = event['start'].get('dateTime', event['start'].get('date'))
#             print(start, event['summary'])
#     except HttpError as error:
#         print('An error occurred: %s' % error)
# if __name__ == '__main__':
#     main()
class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "location", "start_time", "end_time"]
    template_name = "event.html"


########################################################################
# get access to google calendar
########################################################################
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class AcccessToGoogleCalendar:
    # Creates a "token.pkl" Pickelfile when you first try to get in touch with your Google Calendar.....
    def get_token(self):
        creds = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        token = creds.run_local_server(port=0)
        pickle.dump(token, open("token.pkl", "wb"))

    # .....for any future call the token will be simply read from "token.pkl"
    def load_token(self):
        token = pickle.load(open("token.pkl", "rb"))
        return token

    def verify(self):
        if not os.path.exists("token.pkl"):
            self.get_token()
        token = self.load_token()
        enter = build("calendar", "v3", credentials=token)
        return enter


########################################################################
# Methods applicable to Google Calendar Events
########################################################################
class ViewEvent(AcccessToGoogleCalendar, generic.View):
    def get(self, request, *args, **kwargs):
        enter = self.verify()
        member = Member.objects.get(member__pk=request.user.pk)
        events = Event.objects.get_all_events(member=member)
        events_result = (
            enter.events()
            .list(
                calendarId="primary",
            )
            .execute()
        )
        event_dict = {}
        for event in events.values():
            event_dict.update(event)
        e = (
            enter.events()
            .insert(calendarId="primary", sendNotifications=True, body=event_dict)
            .execute()
        )
        events = events_result.get("items", [])
        event_list = []
        for event in events:
            event_list.append(event["id"])
        return event_list


# socialv@django-group.iam.gserviceaccount.com
class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "login"
    template_name = "calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        group = get_object_or_404(
            Group, pk=self.kwargs.get("group_pk", None))
        member = group.group_member.get(member=request.user)
        events = Event.objects.get_all_events(group_pk=group.pk)
        running_events = Event.objects.get_running_events(member=member)
        event_list = []
        print(events)
        print(group)
        context = {"form": forms, "events": events, "group": group, "member": member
                   #    "events_month": events_month
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        group = get_object_or_404(
            Group, pk=self.kwargs.get("group_pk", None))
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            event = form.save()
            # print(event.pk)
            event_title = form.cleaned_data.get("title")
            start_date_data = form.cleaned_data.get("start_time")
            end_date_data = form.cleaned_data.get("end_time")
            description = form.cleaned_data.get("description")
            location = form.cleaned_data.get("location")
            group = get_object_or_404(
                Group, pk=self.kwargs.get("group_pk", None))
            member = group.group_member.get(member=request.user)
            event.member = member
            event.save()
            event = Event.objects.create(member=member, group=group, title=event_title, description=description, location=location,
                                         start_time=start_date_data,
                                         end_time=end_date_data)
            invite = EventInvite.objects.create(event=event)
            group = get_object_or_404(
                Group, pk=self.kwargs.get("group_pk", None))
            members = group.group_member.get(member=request.user)
            notif = Notification.objects.create(
                notification_type="Event Invite", event=event, content_preview="The Group Admin Just Created an Event and you can choose to accept or decline.", group=group)
            if start_date_data > end_date_data:
                messages.add_message(self.request, messages.INFO,
                                     'Please enter the correct period.')
                return HttpResponseRedirect(reverse("calendar-view"))
            else:
                context = {"form": form, "group": group
                           }
                return render(request, self.template_name, context)
            #     service = build_service(self.request)
            #     calendarId = "socialv@django-group.iam.gserviceaccount.com"
            #     event = (
            #         service.events().insert(
            #             calendarId=calendarId,
            #             body={
            #                 "summary": eventTitle,
            #                 "start": {"dateTime": start_date_data.isoformat()},
            #                 "end": {"dateTime": end_date_data.isoformat()},
            #             },
            #         ).execute()
            #     )
    def get_context_data(self, **kwargs):
        context = super(CalendarViewNew, self).get_context_data(**kwargs)
        calendarId = self.request.user.email
        form = EventForm()
        s_event = []
        service = build_service(self.request)
        events = (
            service.events().list(
                calendarId="socialv@django-group.iam.gserviceaccount.com",
            ).execute()
        )
        print(self.kwargs["group_pk"])
        for event in events['items']:
            event_title = event['summary']
            # Deleted the last 6 characters (deleted UTC time)
            start_date_time = event["start"]["dateTime"]
            start_date_time = start_date_time[:-6]
            # Deleted the last 6 characters (deleted UTC time)
            end_date_time = event['end']["dateTime"]
            end_date_time = end_date_time[:-6]
            s_event.append([event_title, start_date_time, end_date_time])
        context = {
            "form": form,
            "booking_event": s_event,
            "group": self.kwargs.get("group_pk", None)
        }
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             'Form submission success!!')
        return redirect('event-list')


class AllEventsListView(ListView):
    """ All event list views """
    template_name = "event_list.html"
    model = Event
    # def get_queryset(self):
    # member = Member.objects.get(member__pk=self.request.user.pk)
    # return Event.objects.get_all_events()


def event_on_calender_view(request):
    pass


def yes_members_view(request, group_pk, event_pk):
    member = Member.objects.get(member__pk=request.user.pk, group__pk=group_pk)
    invite = EventInvite.objects.get(event__pk=event_pk)
    invite.yes.add(member)
    return redirect('event-list')


def no_members_view(request, group_pk, event_pk):
    member = Member.objects.get(member__pk=request.user.pk, group__pk=group_pk)
    invite = EventInvite.objects.get(event__pk=event_pk)
    invite.no.add(member)
    return redirect('event-list')


def maybe_members_view(request, group_pk, event_pk):
    member = Member.objects.get(member__pk=request.user.pk, group__pk=group_pk)
    invite = EventInvite.objects.get(event__pk=event_pk)
    invite.maybe.add(member)
    return redirect('event-list')


def invite_summary(request, event_pk):
    invite = EventInvite.objects.get(pk=event_pk)
    yes_members = invite.yes.all()
    no_members = invite.no.all()
    maybe_members = invite.maybe.all()
    return render(request, "event_summary.html", {
        "yes_members": yes_members,
        "no_members": no_members,
        "maybe_members": maybe_members,
    })


# def create_event(request, group_pk):
#     if request.method == 'POST':
#         form = EventForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data.get('title')
#             description = form.cleaned_data.get('description')
#             start_time = form.cleaned_data.get('start_time')
#             end_time = form.cleaned_data.get('end_time')
#             group = Group.objects.get(group_pk=group_pk)
#             Event.objects.create(creator=request.user, group=group, title=title, description=description,
#                                  start_time=start_time,
#                                  end_time=end_time)
#             return redirect('event-list')
def edit_event(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    event_form = EventForm(instance=event)
    if request.method == 'POST':
        e_form = EventForm(request.POST, instance=event)
        if e_form.is_valid():
            e_form.save()
            return redirect('event-list')
    context = {
        'event_form': event_form
    }
    return render(request, 'calendar.html', context)


class HomeView(FormView):
    form_class = EventForm
    template_name = 'event.html'

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        event = form.save()
        event.member = member
        event.save()
        invite = EventInvite.objects.create(event=event)
        notif = Notification.objects.create(
            notification_type="Event Invite", event=event,
            content_preview="The Group Admin Just Created an Event and you can choose to accept or decline.",
            group=Group.objects.get(pk=self.kwargs["group_pk"]))
        eventTitle = form.cleaned_data.get("title")
        start_date_data = form.cleaned_data.get("start_time")
        end_date_data = form.cleaned_data.get("end_time")
        # member =
        if start_date_data > end_date_data:
            messages.add_message(self.request, messages.INFO,
                                 'Please enter the correct period.')
            return HttpResponseRedirect(reverse("event-list"))
        service = build_service(self.request)
        calendarId = self.request.user.email
        event = (
            service.events().insert(
                calendarId=f'{calendarId}',
                body={
                    "summary": eventTitle,
                    "start": {"dateTime": start_date_data.isoformat()},
                    "end": {"dateTime": end_date_data.isoformat()},
                },
            ).execute()
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        calendarId = self.request.user.email
        form = EventForm()
        s_event = []
        service = build_service(self.request)
        events = (
            service.events().list(
                calendarId="socialv@django-group.iam.gserviceaccount.com",
            ).execute()
        )
        print(self.kwargs["group_pk"])
        for event in events['items']:
            event_title = event['summary']
            # Deleted the last 6 characters (deleted UTC time)
            start_date_time = event["start"]["dateTime"]
            start_date_time = start_date_time[:-6]
            # Deleted the last 6 characters (deleted UTC time)
            end_date_time = event['end']["dateTime"]
            end_date_time = end_date_time[:-6]
            s_event.append([event_title, start_date_time, end_date_time])
        context = {
            "form": form,
            "booking_event": s_event,
            "group": self.kwargs.get("group_pk", None)
        }
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             'Form submission success!!')
        return redirect(reverse('cal:home'))


# @login_required(login_url="login")
# @is_group_admin
def cre(request, group_pk):
    print("bb")
    if request.method == "POST":
        form = EventForm(request.POST or None)
        if form.is_valid():
            member = Member.objects.get(member__pk=request.user.pk)
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            location = form.cleaned_data["location"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            event = Event.objects.get_or_create(
                user=member,
                title=title,
                description=description,
                location=location,
                start_time=start_time,
                end_time=end_time,
            )
            notif = Notification.objects.create(
                notification_type="Event Invite", event=event,
                content_preview="The Group Admin Just Created an Event and you can choose to accept or decline.",
                group=Group.objects.get(pk=group_pk))
            return HttpResponseRedirect(reverse("calendar"))
    form = EventForm()
    return render(request, "event.html", {"form": form})
