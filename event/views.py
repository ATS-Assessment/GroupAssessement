from datetime import timedelta, datetime, date
import calendar
from calendar import HTMLCalendar
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView, DetailView
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from notification.models import Notification
from django.urls import reverse_lazy, reverse


from .models import EventMember, Event
from groups.models import Group, Member
from groups.decorators import is_group_admin
from .utils import Calendar
from .forms import EventForm


# def view_calendar(request, year, month):
#     name = "Sam"
#     month = month.capitalize()
#     month_num = int(list(calendar.month_name).index(month))
#     cal = HTMLCalendar.formatmonth(year, month_num)
#     context = {
#         "name": name,
#         "month": month,
#     }
#     return render(request, "events.html", context)


# def get_date(req_day):
#     if req_day:
#         year, month = (int(x) for x in req_day.split("-"))
#         return date(year, month, day=1)
#     return datetime.today()


# def prev_month(d):
#     first = d.replace(day=1)
#     prev_month = first - timedelta(days=1)
#     month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
#     return month


# def next_month(d):
#     days_in_month = calendar.monthrange(d.year, d.month)[1]
#     last = d.replace(day=days_in_month)
#     next_month = last + timedelta(days=1)
#     month = "month=" + str(next_month.year) + "-" + str(next_month.month)
#     return month


# class CalendarView(LoginRequiredMixin, generic.ListView):
#     login_url = "accounts:signin"
#     model = Event
#     template_name = "calendar.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         d = get_date(self.request.GET.get("month", None))
#         cal = Calendar(d.year, d.month)
#         html_cal = cal.formatmonth(withyear=True)
#         context["calendar"] = mark_safe(html_cal)
#         context["prev_month"] = prev_month(d)
#         context["next_month"] = next_month(d)
#         return context


@login_required(login_url="login")
@is_group_admin
def create_event(request, group_pk):
    form = EventForm(request.POST or None)
    member = Member.objects.get(pk=request.user.pk)
    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        location = form.cleaned_data["location"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=member,
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
        )
        notif = Notification.objects.create(
            notification_type="invite", content_preview="The Group Admin Just Created an Event and ", group=Group.objects.get(pk=group_pk))
        return HttpResponseRedirect(reverse("calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "location", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    member = Member.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


# def add_eventmember(request, event_id):
#     forms = AddMemberForm()
#     if request.method == "POST":
#         forms = AddMemberForm(request.POST)
#         if forms.is_valid():
#             member = EventMember.objects.filter(event=event_id)
#             event = Event.objects.get(id=event_id)
#             if member.count() <= 9:
#                 user = forms.cleaned_data["user"]
#                 EventMember.objects.create(event=event, user=user)
#                 return redirect("calendarapp:calendar")
#             else:
#                 print("--------------User limit exceed!-----------------")
#     context = {"form": forms}
#     return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "login"
    template_name = "calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        # events = Event.objects.get_all_events(user=request.user)
        # events_month = Event.objects.get_running_events(user=request.user)
        # event_list = []
        # # start: '2020-09-16T16:00:00'
        # for event in events:
        #     event_list.append(
        #         {
        #             "title": event.title,
        #             "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        #             "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

        #         }
        #     )
        context = {"form": forms, "events": event_list,
                   #    "events_month": events_month
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)


class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)


def event_on_calender_view(request):
    pass


def yes_members(request, member_pk):

    pass


def no_members(request, member_pk):
    pass


def maybe_members(request, member_pk):
    pass


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
