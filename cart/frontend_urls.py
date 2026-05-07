from django.urls import path
from . import views_frontend

urlpatterns = [
    path('', views_frontend.cart_detail, name='cart_detail'),
    path('checkout/', views_frontend.checkout, name='checkout'),
]
