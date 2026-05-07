"""
URL configuration for EnerPulse MLM platform.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language

# Admin site customization
admin.site.site_header = 'EnerPulse 會員管理'
admin.site.site_title = 'EnerPulse 管理後台'
admin.site.index_title = 'EnerPulse 管理系統'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('i18n/setlang/', set_language, name='set_language'),
    path('api/auth/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/wallet/', include('wallet.urls')),
    path('api/mlm/', include('mlm.urls')),
    path('api/payment/', include('payment.urls')),
    # Frontend routes
    path('', include('accounts.frontend_urls')),
    path('products/', include('products.frontend_urls')),
    path('cart/', include('cart.frontend_urls')),
    path('orders/', include('orders.frontend_urls')),
    path('wallet/', include('wallet.frontend_urls')),
    path('mlm/', include('mlm.frontend_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
