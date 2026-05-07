from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    """Compact serializer for product lists."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'display_name', 'slug', 'sku', 'price_usd', 'pv',
            'stock', 'is_active', 'is_featured',
            'image', 'category', 'category_name',
        ]
    
    def get_display_name(self, obj):
        return obj.get_name()


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full product details with language support."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    display_name = serializers.SerializerMethodField()
    display_description = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_display_name(self, obj):
        return obj.get_name()
    
    def get_display_description(self, obj):
        return obj.get_description()
