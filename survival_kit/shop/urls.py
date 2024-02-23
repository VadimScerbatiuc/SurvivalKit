from django.urls import path

from .views import *


urlpatterns = [
    path('', ShopBasePageView.as_view(), name='main_page'),
]