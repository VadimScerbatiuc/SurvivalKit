from rest_framework import generics
from shop.models import Product
from shop.api.serializers import ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer