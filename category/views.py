from django.shortcuts import render

# returns the cart-page
def cart(request):
    return render (request, 'store/cart.html')
