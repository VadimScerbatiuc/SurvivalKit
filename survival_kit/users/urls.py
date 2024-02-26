from django.urls import path

from .views import *


app_name = 'users'

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('sign_in/', SignInView.as_view(), name='sign_in'),
    path('logout/', SignoutView.as_view(), name='sign_out'),
]
