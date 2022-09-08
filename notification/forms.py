from dataclasses import field
from pyexpat import model
from django import forms
from .models import Event, Poll


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_date", "end_date"]


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["title", ]
