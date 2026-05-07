from products.models import Product, Category


def featured_products(request):
    """提供精選商品給所有模板（用於首頁等）。"""
    return {
        'featured_products': Product.objects.filter(
            is_active=True, is_featured=True
        ).select_related('category')[:6],
        'product_categories': Category.objects.filter(is_active=True),
    }
