from django import forms
from .models import *

class CreateProductForm(forms.Form):
    name = forms.CharField(label='Name')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category')
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Brand')
    price = forms.DecimalField(label='Price')
    description = forms.CharField(label='Desctiption')
    stock = forms.IntegerField(label='Stock')

    class Meta:
        model = Product