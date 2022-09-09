from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", 'email', 'image']
