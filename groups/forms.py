from .models import Group
from django import forms


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "privacy_status", "group_image"]
