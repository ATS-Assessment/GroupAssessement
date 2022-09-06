from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import UserProfile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def clean(self):
        super(RegisterForm, self).clean()
        data = self.cleaned_data.get('email')

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email is already exist.')


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
