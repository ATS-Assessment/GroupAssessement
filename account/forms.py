from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import UserGroup, UserProfile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class GroupForm(ModelForm):
    class Meta:
        model = UserGroup
        fields = ['name', 'is_closed']


class AddMemberToAdminForm(forms.Form):
    username = forms.CharField(max_length=200)
    group_name = forms.CharField(max_length=200)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']