from django.contrib import admin

from .models import *


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductPriceInline]


@admin.register(Category)
class Category(admin.ModelAdmin):
    pass


@admin.register(Brand)
class Brand(admin.ModelAdmin):
    pass




