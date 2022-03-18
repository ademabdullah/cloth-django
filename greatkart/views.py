from django.shortcuts import render
from store.models import Product

''' This method enables a list of
    products to be passed to the
    homepage template'''

def home (request):
    products = Product.objects.all().filter(is_available = True)

    context = {
        'products': products,
    }
    return render(request, 'Home.html', context)
