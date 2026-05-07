from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def product_list(request):
    """Product listing page."""
    return render(request, 'products/product_list.html')


def product_detail(request, product_id):
    """Product detail page."""
    return render(request, 'products/product_detail.html', {
        'product_id': product_id,
    })
