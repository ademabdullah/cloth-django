from django.urls import path
from . import views

''' The pathways withtin the carts application,
    naming view methods enables URL reversing and this
    enables dynamic URLs to be created'''

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name = 'add_cart'),
    path('subtract_cart/<int:product_id>/', views.subtract_cart_item, name = 'subtract_cart_item'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('checkout/', views.checkout, name = 'checkout'),
              ]
