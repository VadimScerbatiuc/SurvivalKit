from django.urls import path, include

from .views import *


app_name = 'shop'

# urlpatterns = [
#     path('', ShopBasePageView.as_view(), name='main_page'),
#     path('products_page/', ProductPageView.as_view(), name='product_page'),
#     path('products_list/', ProductListView.as_view(), name='product_list'),
#
#     path('cart/', CartView.as_view(), name='cart_view'),
#     path('product-create/', ProductCreateView.as_view(), name="product_create"),
#     path('product-detail/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
#     path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
#     path('success/', SuccessView.as_view(), name="success-payment"),
#     path('cansel/', CancelView.as_view(), name="cancel-payment"),
#
# ]

product_urls = [
    path('page/', ProductPageView.as_view(), name='page'),
    path('list/', ProductListView.as_view(), name='list'),
    path('create/', ProductCreateView.as_view(), name="create"),
    path('detail/<slug:product_slug>/', ProductDetailView.as_view(), name='detail'),
]

stripe_urls = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('success/', SuccessView.as_view(), name="success-payment"),
]

urlpatterns = [
    path('', ShopBasePageView.as_view(), name='main_page'),
    path('cart/', CartView.as_view(), name='cart'),
    path('product/', include((product_urls, 'product'))),
    path('stripe/', include((stripe_urls, 'stripe'))),
]