from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from users.models import UserAccount


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Firs Name')
    last_name = forms.CharField(label='Last Name')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Confirm Password')

    class Meta:
        model = UserAccount
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class SignInForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Passwors')
