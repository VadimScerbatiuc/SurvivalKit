from django import forms
from .models import *


class ProductCreateForm(forms.ModelForm):
    name = forms.CharField(label='Name')
    description = forms.CharField(label='Desription')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', empty_label="Choose category")
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Brand', empty_label="Choose brand")
    price = forms.DecimalField(label='Price')
    stock = forms.IntegerField(label='Stock')
    is_active = forms.BooleanField(label='Is Active')
    image = forms.ImageField(label='Main Photo')

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'brand', 'price', 'stock', 'is_active']

    def save(self, commit=True):
        product = super().save(commit=commit)

        image_file = self.cleaned_data.get('image')
        print(image_file)
        if image_file:
            ProductImage.objects.create(product=product, image=image_file)

        return product