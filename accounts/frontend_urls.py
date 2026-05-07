from django.urls import path
from . import views_frontend
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views_frontend.home, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        next_page='/'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views_frontend.register_view, name='register'),
    path('profile/', views_frontend.profile_view, name='profile'),
]
