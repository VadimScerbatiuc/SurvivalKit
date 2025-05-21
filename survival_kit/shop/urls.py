from django.urls import path, include

from .views import *


app_name = 'shop'

product_urls = [
    path('list/', ProductListView.as_view(), name='list'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('detail/<slug:product_slug>/', ProductDetailView.as_view(), name='detail'),
]

stripe_urls = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', SuccessView.as_view(), name='success-payment'),
    path('webhooks/', my_webhook_view, name='webhook')
]

urlpatterns = [
    path('', ProductPageView.as_view(), name='main_page'),
    path('cart/', CartView.as_view(), name='cart'),
    path('product/', include((product_urls, 'product'))),
    path('stripe/', include((stripe_urls, 'stripe'))),
]