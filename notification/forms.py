from dataclasses import field
from pyexpat import model
from django import forms
from .models import Event,  Notification, Poll


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_date", "end_date"]


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["title", ]


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["yes", "no", "maybe"]
