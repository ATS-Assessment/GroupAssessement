from dataclasses import field
from pyexpat import model
from django import forms
from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["yes", "no", "maybe"]
