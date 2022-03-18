from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q

'''
    The following 2 links provide information
    on how to use Q objects for complex queries
    https://docs.djangoproject.com/en/4.0/topics/db/queries/
    https://books.agiliq.com/projects/django-orm-cookbook/en/latest/query_relatedtool.html
 '''


''' if a category_slug is provided, displayed all the products that have
    that category slug, else display all products.
    Products are displayed using a paginater (4 products per page with
    navigation provided) '''

def store (request, category_slug = None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug) # get the category from the category_slug
        products = Product.objects.filter (category = categories, is_available = True)
        paginator = Paginator(products, 4) # 4 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) # 4 products a page
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 4) # 4 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)  # 4 products a page, points to all pages
        product_count = products.count() # counts the number of products

    context = {
        'products': paged_products,
        'product_count': product_count
    }

    # products and product count passed to the store page
    return render(request, 'store/store.html', context)


''' Get the product that where the category slug and product slug match,
    pass this product to the product detail page '''

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
              }

    return render(request, 'store/product_detail.html', context)


''' when searching for a product, if the keyword typed in the search bar
    exists in a product_name or in a product description, the product(s) will
    be displayed on the store page '''


def search (request):
    if 'keyword' in request.GET: #check if GET request has a keyword attribute
        keyword = request.GET['keyword'] # if it does store its value
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) ) #if the descripton contains the keyword
            product_count = products.count()
    context = {'products': products, 'product_count' : product_count}
    return render(request, 'store/store.html', context)
