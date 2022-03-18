from . import views
from django.urls import path


''' The pathways for the store app, each path has a view-method that is named
    to allow URL-reversing to occur, get_url method enables slugs to be passed
    to the view-method when URL-reversing occurs, these slugs appear in the URL
'''

urlpatterns = [
    path ('', views.store , name='store'),
    path ('category/<slug:category_slug>/', views.store , name = 'products_by_category'),
    path ('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail , name = 'product_detail'),
    path ('search/', views.search, name = 'search'),
              ]
