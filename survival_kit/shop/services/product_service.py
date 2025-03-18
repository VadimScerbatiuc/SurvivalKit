from shop.models import Product

class ProductService:
    def get_filtered_products(self, request):
        queryset = Product.objects.all()
        if request.GET.getlist('category'):
            queryset = queryset.filter(category__slug__in=request.GET.getlist('category'))
        if request.GET.get('brand'):
            queryset = queryset.filter(brand__slug__in=request.GET.getlist('brand'))
        if request.GET.get('search'):
            queryset = queryset.filter(name__icontains=request.GET.get('search'))

        return queryset