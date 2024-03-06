from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from shop.models import Product, ProductPrice


class ShopBasePageView(View):
    template_name = 'base.html'

    def get(self, request):
        return render(request, self.template_name)


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
