from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

# urlpatterns = [
#     path('favorite/', views.toggle_favorite, name='toggle_favorite'),
    
#     # Standard Django Login/Logout
#     # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('register/', views.register_view, name='register'),
    
#     path('login/', auth_views.LoginView.as_view(
#         template_name='login.html',
#         redirect_authenticated_user=True
#     ), name='login'),
    
#     path('logout/', auth_views.LogoutView.as_view(
#         next_page='menu:menu_view'
#     ), name='logout'),
    
# ]
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('verify/', views.verify_otp_view, name='verify_otp'),
    path('profile/', views.profile_view, name='profile'), # NEW
    path('logout/', auth_views.LogoutView.as_view(next_page='menu:menu_view'), name='logout'),
    path('favorite/', views.toggle_favorite, name='toggle_favorite'),
]
