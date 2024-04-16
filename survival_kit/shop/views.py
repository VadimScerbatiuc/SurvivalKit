import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse

from shop.models import Product, Category, Brand, CartItem


class ShopBasePageView(View):
    template_name = 'base.html'

    def get(self, request):

        return render(request, self.template_name)


class ProductPageView(View):
    model = Product
    template_name = 'shop/product_page.html'
    context_object_name = 'products'

    def get_queryset(self, request):
        queryset = Product.objects.all()
        if request.GET.getlist('category'):
            queryset = queryset.filter(category__slug__in=request.GET.getlist('category'))
        if request.GET.get('brand'):
            queryset = queryset.filter(brand__slug__in=request.GET.getlist('brand'))

        return queryset

    def get(self, request):
        categories = Category.objects.all()
        brands = Brand.objects.all()
        active_categories = request.GET.getlist('category')
        active_brands = request.GET.getlist('brand')
        return render(
            request,
            self.template_name,
            {
                self.context_object_name: self.get_queryset(request),
                'categories': categories,
                'brands': brands,
                'active_categories': active_categories,
                'active_brands': active_brands,
            }
        )


class ProductListView(View):
    model = Product
    template_name = 'shop/includes/product_list.html'
    context_object_name = 'products'

    def get_queryset(self, request):
        queryset = Product.objects.all()
        if request.GET.getlist('category'):
            queryset = queryset.filter(category__slug__in=request.GET.getlist('category'))
        if request.GET.get('brand'):
            queryset = queryset.filter(brand__slug__in=request.GET.getlist('brand'))

        return queryset

    def get(self, request):

        return render(
            request,
            self.template_name,
            {self.context_object_name: self.get_queryset(request)}
        )


class CartView(View):
    model = CartItem
    template_name = 'shop/cart_list.html'
    context_object_name = 'cart'

    def get_queryset(self, request):
        queryset = CartItem.objects.filter(user=request.user)

        return queryset

    def get(self, request):

        return render(
            request,
            self.template_name,
            {
                self.context_object_name: self.get_queryset(request)
            }
        )

    def post(self, request):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 0))
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        new_quantity = cart_item.quantity + quantity

        if new_quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = new_quantity
            cart_item.save()

        return JsonResponse(
            data={'status': 'success'},
            status=200
        )
