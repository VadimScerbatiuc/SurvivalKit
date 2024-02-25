from django.urls import path, include

from .views import *


app_name = 'shop'

urlpatterns = [
    path('', ShopBasePageView.as_view(), name='main_page'),
]
