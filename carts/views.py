from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

''' A private method for returning the session key,
    the session key is used to uniquely identify each
    cart
'''

def _cart_id (request): # private method for returning the session key
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


''' A method for adding items to the cart,
    the method takes in a product_id,
    if the product already exists as a cart-item
    within the cart, increase it's quantity by one '''


def add_cart(request, product_id):

    product = Product.objects.get(id=product_id) # get the product via its product_ID

    # point to the existing cart, else create a cart
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist: # create a cart
        cart = Cart.objects.create(
        cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get (product=product, cart=cart)
        cart_item.quantity += 1 # cart_item.quantity = += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
        product = product,
        quantity = 1,
        cart = cart,
        )
        cart_item.save()
    return redirect('cart') # redirects to the cart page (creates a HttpResponse object)

''' A method for subtracting items from the cart,
    decrement the cart_items quantity by one,
    if quantity falls to 0, delete the cart_item'''

def subtract_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request)) # get or create the cart
    product = get_object_or_404(Product, id = product_id) #get the product
    cart_item = CartItem.objects.get(product=product, cart = cart)
    if cart_item.quantity > 1: #only able to decrement if item quantity is >1
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete() # delete the cart item if quanity == 1
    return redirect('cart')

def subtract_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart = cart)
    cart_item.delete()
    return redirect ('cart')

'''The following method loops through the items in the cart,
    calculates the total, the tax, and passes these
    (aswell as cart_items) to the store/cart template'''

def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id = _cart_id(request)) # point to the cart
        cart_items = CartItem.objects.filter(cart = cart, is_active=True)

        # Look through the items in the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) # calculating total
            quantity += cart_item.quantity
        tax = 0.2 * total
        grand_total = total + tax
    except ObjectNotExist: # no objects in the cart
        pass # do nothing


    context = {
        'total':total,
        'quantity':quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
              }

    return render(request, 'store/cart.html', context)  # Creates a Http Response Object
                                                        #makes the dictionary-data available
                                                        #in the template'''
