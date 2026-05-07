from rest_framework import viewsets, permissions
from .models import Product, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Product listing and detail API."""
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        # Filter by category
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        # Filter featured
        if self.request.query_params.get('featured'):
            qs = qs.filter(is_featured=True)
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
