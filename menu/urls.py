# urls.py example

from django.urls import path
from . import views

app_name = 'menu' # Ensure your app is named 'menu' for URL lookups

urlpatterns = [
    # Main Menu View
    path('', views.menu_view, name='menu_view'),
    
    # AJAX Endpoint
    path('add-to-cart/', views.add_to_basket_api, name='add_to_basket_api'), 
    
    # Standard Basket Views
    path('basket/', views.view_basket, name='basket'),
    path('basket/clear/', views.clear_basket, name='clear_basket'),
    path('update-cart/', views.update_basket_api, name='update_basket_api'),
]