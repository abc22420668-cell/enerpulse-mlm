from django.urls import path
from . import views_frontend

urlpatterns = [
    path('', views_frontend.mlm_dashboard, name='mlm_dashboard'),
    path('tree/', views_frontend.mlm_tree, name='mlm_tree'),
    path('bonuses/', views_frontend.mlm_bonuses, name='mlm_bonuses'),
]
