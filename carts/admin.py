from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

''' Registering models here allows the developer to access,
    modify and create instances in Django's admin GUI backend'''

admin.site.register(Cart)
admin.site.register(CartItem)
