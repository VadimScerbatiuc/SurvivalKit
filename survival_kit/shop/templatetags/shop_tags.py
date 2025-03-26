from django import template
from shop.models import *

register = template.Library()

@register.simple_tag()
def currency_symbol():
    price_setting = PriceSetting.objects.get(is_active=True)
    return price_setting.currency_symbol