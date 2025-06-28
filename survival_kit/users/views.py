import json

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from users.forms import SignUpForm, SignInForm
from .models import UserAccount


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/sign_up.html'
    success_url = reverse_lazy('users:sign_in')


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'users/sign_in.html'

    def get_success_url(self):
        return reverse_lazy('shop:main_page')


class SignOutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:sign_in')


class ManagementPageView(LoginRequiredMixin, View):
    template_name = "users/management_page.html"

    def get(self, request):
        all_users = UserAccount.objects.all()
        return render(
            request,
            self.template_name,
            {
                "all_users": all_users,
            }
        )

    def post(self, request):
        data = json.loads(request.body)
        user_id = data.get("user_id")
        new_role = data.get("role")
        UserAccount.objects.filter(id=user_id).update(role=new_role)

        return JsonResponse(
            data={
                'status': 'success',
            },
            status=200
        )