from django.urls import path
from . import views

''' The pathways withtin the carts application,
    naming view methods enables URL reversing and this
    enables dynamic URLs to be created'''
    
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name = 'add_cart'),
    path('subtract_cart/<int:product_id>/', views.subtract_cart, name = 'subtract_cart'),
    path('remove_cart_item/<int:product_id>/', views.subtract_cart, name = 'remove_cart_item'),
              ]
