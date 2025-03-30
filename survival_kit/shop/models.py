from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse

from users.models import UserAccount


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True,)
    slug = AutoSlugField(
        populate_from='name',
        max_length=200,
        db_index=True,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True,)
    slug = AutoSlugField(
        populate_from='name',
        max_length=200,
        db_index=True,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(
        populate_from='name',
        max_length=200,
        db_index=True,
        unique=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product:product_detail', args=[self.slug])

    @property
    def main_image(self):
        main_image = ProductImage.objects.filter(product=self).first()

        return main_image


class PriceSetting(models.Model):
    is_active = models.BooleanField(default=True)
    currency_code = models.CharField(max_length=10, blank=False, null=False)
    currency_symbol = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Price Stettings"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='images/', blank=True, null=False)
    order = models.PositiveIntegerField(default=1, blank=True, null=False)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Product Images"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(UserAccount, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def price_by_quantity(self):
        return self.product.price * self.quantity
