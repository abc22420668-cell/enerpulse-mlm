from django.urls import path
from . import views_frontend

urlpatterns = [
    path('', views_frontend.wallet_dashboard, name='wallet_dashboard'),
    path('transactions/', views_frontend.wallet_transactions, name='wallet_transactions'),
    path('withdraw/', views_frontend.wallet_withdraw, name='wallet_withdraw'),
]
