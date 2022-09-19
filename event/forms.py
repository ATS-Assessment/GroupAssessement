
from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "description", "location",
                  "start_time", "end_time",)
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "Location": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event Location",
                }
            ),
            "start_time": forms.DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": forms.DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]
