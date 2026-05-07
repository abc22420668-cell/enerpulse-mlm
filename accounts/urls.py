from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, register_view

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # CSRF-safe register (outside router, pure Django view)
    path('user/register/', register_view, name='register_api'),
]
