from django.shortcuts import render
from django.views import View

from shop.models import Product, Category, Brand


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
