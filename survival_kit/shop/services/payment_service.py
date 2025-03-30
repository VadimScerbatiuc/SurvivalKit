from shop.models import CartItem, PriceSetting

class PaymentService:
    def __init__(self, user):
        self.user = user

    def get_products_data_for_stripe(self):
        cart_items = CartItem.objects.filter(user=self.user)
        currency_obj = PriceSetting.objects.get(is_active=True)
        products_data = []

        for cart_item in cart_items:
            products_data.append(
                {
                    'price_data': {
                        'currency': currency_obj.currency_code,
                        'product_data': {
                            'name': cart_item.product.name
                        },
                        'unit_amount': int(cart_item.product.price * 100)
                    },
                    'quantity': cart_item.quantity,
                }
            )
        return products_data