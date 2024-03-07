from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from users.forms import SignUpForm, SignInForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/sign_up.html'
    success_url = reverse_lazy('users:sign_in')


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'users/sign_in.html'

    def get_success_url(self):
        return reverse_lazy('shop:main_page')


class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:sign_in')
