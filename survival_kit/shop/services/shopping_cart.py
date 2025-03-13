from shop.models import CartItem, PriceSetting

class CartService:
    def __init__(self, user):
        self.user = user

    def get_total_price(self):
        cart_items = CartItem.objects.filter(user=self.user)
        total_price = 0

        for cart_item in cart_items:
            total_price += cart_item.price_by_quantity

        return total_price

    def get_price_setting(self):
        # TODO: Move this to 'templatetags' to be able to render price currency on all templates
        return PriceSetting.objects.filter(is_active=True)
