from django.urls import path, include

from .views import *


app_name = 'shop'

urlpatterns = [
    path('', ShopBasePageView.as_view(), name='main_page'),
    path('all-products/', ProductListView.as_view(), name='product_list')
]
