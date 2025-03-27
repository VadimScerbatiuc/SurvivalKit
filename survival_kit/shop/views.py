import json

import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.views.generic import DetailView, CreateView, TemplateView

from shop.forms import ProductCreateForm
from shop.models import Product, Category, Brand, CartItem
from shop.services.shopping_cart import CartService
from shop.services.product_service import ProductService


class ShopBasePageView(View):
    template_name = 'base.html'

    def get(self, request):
        return render(request, self.template_name)


class ProductPageView(View):
    model = Product
    template_name = 'shop/product_page.html'
    context_object_name = 'products'
    filtered_products = ProductService()

    def get(self, request):
        categories = Category.objects.all()
        brands = Brand.objects.all()
        active_categories = request.GET.getlist('category')
        active_brands = request.GET.getlist('brand')
        return render(
            request,
            self.template_name,
            {
                self.context_object_name: self.filtered_products.get_filtered_products(request),
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
    filtered_products = ProductService()
    def get(self, request):

        return render(
            request,
            self.template_name,
            {self.context_object_name: self.filtered_products.get_filtered_products(request)}
        )


class CartView(View):
    model = CartItem
    template_name = 'shop/cart_list.html'
    context_object_name = 'cart'

    def get_queryset(self, request):
        queryset = CartItem.objects.filter(user=request.user)

        return queryset

    def get(self, request):
        cart_service = CartService(request.user)
        return render(
            request,
            self.template_name,
            {
                self.context_object_name: self.get_queryset(request),
                'total_price': cart_service.get_total_price()
            }
        )

    def post(self, request):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 0))
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        new_quantity = cart_item.quantity + quantity
        price_by_quantity = cart_item.product.price * new_quantity
        cart_service = CartService(request.user)

        if new_quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = new_quantity
            cart_item.save()

        queryset_isempty = not bool(self.get_queryset(request))

        return JsonResponse(
            data={
                'status': 'success',
                'queryset_isempty': queryset_isempty,
                'price_by_quantity': price_by_quantity,
                'total_price': cart_service.get_total_price(),
            },
            status=200
        )


class ProductCreateView(CreateView):
    form_class = ProductCreateForm
    template_name = 'shop/product_create.html'
    success_url = reverse_lazy('shop:product_page')


class ProductDetailView(DetailView):
    model = Product
    templa_name = 'shop/product_detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        product_slug = self.kwargs["product_slug"]
        product = Product.objects.get(slug=product_slug)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': "USD",
                        'product_data': {
                            'name': product.name
                        },
                        'unit_amount': int(product.price * 100)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + 'success/',
            cancel_url=YOUR_DOMAIN + 'cancel/',
        )

        return redirect(checkout_session.url, code=303)


class SuccessView(TemplateView):
    template_name = "shop/success.html"

class CancelView(TemplateView):
    template_name = "shop/cancel.html"