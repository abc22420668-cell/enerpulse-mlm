from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def cart_detail(request):
    """Shopping cart page."""
    return render(request, 'cart/cart_detail.html')


def checkout(request):
    """Checkout page."""
    return render(request, 'cart/checkout.html')
