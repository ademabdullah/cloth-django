from django.urls import path
from . import views

''' The pathways withtin the carts application,
    naming view methods enables URL reversing and this
    enables dynamic URLs to be created'''

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('', views.dashboard, name = 'dashboard'),
                ]
