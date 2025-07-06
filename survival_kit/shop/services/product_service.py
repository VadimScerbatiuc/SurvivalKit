from django.db.models import OuterRef, Exists
from shop.models import Product, FavoriteProduct


class ProductService:
    @staticmethod
    def get_filtered_products(request):
        favorite_product = FavoriteProduct.objects.filter(user=request.user, product=OuterRef('id'))
        queryset = Product.objects.annotate(is_favorite=Exists(favorite_product))
        if request.GET.getlist('category'):
            queryset = queryset.filter(category__slug__in=request.GET.getlist('category'))
        if request.GET.get('brand'):
            queryset = queryset.filter(brand__slug__in=request.GET.getlist('brand'))
        if request.GET.get('search'):
            queryset = queryset.filter(name__icontains=request.GET.get('search'))

        return queryset