from django import forms
from django.forms import ModelForm

from .models import Poll


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["title", "start_date"]
