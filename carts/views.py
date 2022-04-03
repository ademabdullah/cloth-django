from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

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
    current_user = request.user
    product = Product.objects.get(id=product_id) # get the product via its product_ID

    # if the user is authenticated
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            # cart_item = CartItem.objects.filter(product=product, user=current_user)
            item = CartItem.objects.get(product=product, user=current_user)
            item.quantity += 1
            item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            cart_item.save()
        return redirect('cart')

    else: # in the guest view


        # below code points to the existing cart or creates a new one
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        # is the item in the cart
        is_cart_item_exists = CartItem.objects.filter(product=product, cart = cart).exists()
        if is_cart_item_exists:
            item = CartItem.objects.get(product=product, cart = cart)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart = cart)
            item.save()
        return redirect('cart')




''' This decrements the quantity of the item in the kart,
    once this reaches 0, the cart item is deleted '''
def subtract_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # only runs when not logged in
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  #only able to decrement if item quantity is >1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


''' This removes the item from the cart,
    the functionality behind the remove button'''
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


'''The following method loops through the items in the cart,
    calculates the total, the tax, and passes these
    (aswell as cart_items) to the store/cart template'''
def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
              }
    return render(request, 'store/cart.html', context)  # Creates a Http Response Object
                                                        #makes the dictionary-data available
                                                        #in the template'''

@login_required(login_url = 'login')
def checkout (request, total = 0, quantity = 0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
              }
    return render(request, 'store/checkout.html', context)
