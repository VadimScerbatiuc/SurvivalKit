from django.urls import path, include
from .api.views import ProductListAPIView
from .views import *


app_name = 'shop'

product_urls = [
    path('list/', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name="product_create"),
    path('favorites/', FavoriteProductsView.as_view(), name="favorite_products"),
    path('detail/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),

]

urlpatterns = [
    path('product/', include((product_urls, 'product'))),
    path('', ProductPageView.as_view(), name='product_page'),
    path('cart/', CartView.as_view(), name='cart'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('success/', SuccessView.as_view(), name="success-payment"),
    path('api/v1/productlist/', ProductListAPIView.as_view(), name="api")
]