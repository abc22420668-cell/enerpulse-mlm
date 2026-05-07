from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.cart_add, name='cart_add'),
    path('update/', views.cart_update, name='cart_update'),
    path('remove/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('view/', views.cart_view, name='cart_view'),
]
