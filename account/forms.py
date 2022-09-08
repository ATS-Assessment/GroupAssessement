from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import User, UserProfile


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        # widgets = {
        #     'first_name': {'class': 'form_control', 'placeholder': 'Enter your first name'},
        #     'last_name': {'class': 'form_control', 'placeholder': 'Enter your last name'},
        #     'username': {'class': 'form_control', 'placeholder': 'Enter your username'},
        #     'email': {'class': 'form_control', 'placeholder': 'Enter your email'},
        #     'password1': {'class': 'form_control', 'placeholder': 'Enter your password'},
        #     'password2': {'class': 'form_control', 'placeholder': 'Enter your password again'}



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_pix", "location", "phone_number"]
