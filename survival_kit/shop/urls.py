from django.urls import path, include

from .views import *


app_name = 'shop'

urlpatterns = [
    path('', ShopBasePageView.as_view(), name='main_page'),
    path('products_page/', ProductPageView.as_view(), name='product_page'),
    path('products_list/', ProductListView.as_view(), name='product_list'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('product-create/', ProductCreateView.as_view(), name="product_create"),
    path('product-detail/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
]
