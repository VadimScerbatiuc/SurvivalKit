from django import forms
from .models import *
# TODO: empty lines???
class ProductForm(forms.Form):
    name = forms.CharField(label='Name')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category')
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Brand')
    price = forms.DecimalField(label='Price')
    description = forms.CharField(label='Desctiption')
    stock = forms.IntegerField(label='Stock')

    class Meta:
        model = Product


class ProductCreateForm(forms.ModelForm):
    name = forms.CharField(label='Name')
    description = forms.CharField(label='Desription')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category')
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Brand')
    price = forms.DecimalField(label='Price')

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'brand', 'price']
