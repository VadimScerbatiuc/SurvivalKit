from django import forms
from .models import *


class ProductCreateForm(forms.ModelForm):
    name = forms.CharField(label='Name')
    description = forms.CharField(label='Desription')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category')
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Brand')
    price = forms.DecimalField(label='Price')

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'brand', 'price']
