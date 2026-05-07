from django.urls import path
from . import views_frontend

urlpatterns = [
    path('', views_frontend.product_list, name='product_list'),
    path('<int:product_id>/', views_frontend.product_detail, name='product_detail'),
]
