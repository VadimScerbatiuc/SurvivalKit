import json

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse

from shop.forms import ProductCreateForm, ProductForm
from shop.models import Product, Category, Brand, CartItem
from shop.services import *
from shop.services.shopping_cart import CartService
from django.db.models import Q


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
        if request.GET.get('search'):
            queryset = queryset.filter(name__icontains=request.GET.get('search'))

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
        if request.GET.get('search'):
            queryset = queryset.filter(name__icontains=request.GET.get('search'))
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
        services1 = CartService(request.user)
        return render(
            request,
            self.template_name,
            {
                self.context_object_name: self.get_queryset(request),
                'total_price': services1.get_total_price(),
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
        services1 = CartService(request.user)

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
                'total_price': services1.get_total_price(),
            },
            status=200
        )

class RememberAll(View):
    model = Product
    template_name = 'shop/remember.html'
    context_object_name = 'remember'
    form_class = ProductForm()
    brands_list = Brand.objects.all()
    categories_list = Category.objects.all()

    def get_queryset(self, request):
        queryset = Product.objects.filter(pk__gte=4)

        return queryset

    def get(self, request):
        services1 = CartService(request.user)

        return render(
            request,
            self.template_name,
            {
                self.context_object_name: self.get_queryset(request),
                'form': self.form_class,
                'brands_list': self.brands_list,
                'categories_list': self.categories_list,
                'service1': services1.get_price_by_quantity()
            }
        )

    def post(self, request):
        create_product_form = ProductForm(request.POST)
        template_name = 'shop/remember.html'

        if create_product_form.is_valid():
            try:
                Product.objects.create(**create_product_form.cleaned_data)
                return redirect('remember')
            except:
                create_product_form.add_error(None,'Oshibka blia')

        return render(
            request,
            template_name,
            {
                'form': self.form_class,
                'brands_list': self.brands_list,
                'categories_list': self.categories_list,
                'categories_list': self.categories_list,
                self.context_object_name: self.get_queryset(request),
            })


class ProductCreateView(View):
    model = Product
    template_name = 'shop/product_create.html'
    form_class = ProductCreateForm
    context_object_name = 'new_product'

    def get(self, request):

        return render(
            request,
            self.template_name,
            {
                'form': self.form_class,
            }
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

        return render(
            request,
            self.template_name,
            {
                'form': form,

            }
        )


class ImproveView(View):
    model = Product
    template_name = 'shop/improve.html'
    content_object_name = 'products'
    form_class = ProductCreateForm

    paginator = Paginator(model.objects.all(), 1)

    def get(self, request):
        page_number = request.GET.get('page')
        page_object = self.paginator.get_page(page_number)


        return render(
            request,
            self.template_name,
            {
                self.content_object_name: self.model.objects.all(),
                'form': self.form_class,
                'page_object': page_object,
            }
        )

    def post(self, request):

        return render(
            request,
            self.template_name,
            {
                'form': self.form_class,
            }
        )

def search(request):

    if request.method == "POST":
        searched = request.POST.get('searched')
        outputt = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        return render(
            request,
            "shop/search.html",

            {
                'searched': searched,
                'filtresult': outputt
            }
        )

    else:
        return render(
            request,
            "shop/search.html",
            {}
        )