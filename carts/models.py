from django.db import models
from store.models import Product
from accounts.models import Account

''' The cart_id class is
    linked the session key '''

class Cart(models.Model):
    cart_id = models.CharField(max_length = 250, blank = True)
    date_added = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.cart_id

'''
    The cart_item class has a quantity and
    each cart_item is a product that can belong
    to a cart, it also can belong to a user (but guest
    users can still add items to their cart),
    1 cart has 0.* cart items and there is a
    1 to 1 relationship between cart_item and product
'''


class CartItem(models.Model):
    product = models.ForeignKey (Product, on_delete=models.CASCADE)
    cart = models.ForeignKey (Cart, on_delete = models.CASCADE, null = True)
    quantity = models.IntegerField()
    is_active = models.BooleanField (default=True)
    user = models.ForeignKey(Account, on_delete = models.CASCADE,null = True) # if user account is deleted, cart_item is deleted also

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name
