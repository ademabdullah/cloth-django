from . import views
from django.urls import path


''' The pathways for the store app, each path has a view-method that is named
    to allow URL-reversing to occur, get_url method enables slugs to be passed
    to the view-method when URL-reversing occurs, these slugs appear in the URL
'''

urlpatterns = [
    path ('place_order/', views.place_order, name='place_order'),
    path ('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
              ]
