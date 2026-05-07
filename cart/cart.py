"""
Session-based shopping cart for EnerPulse.

Cart structure in session:
    cart = {
        "items": {
            "1": {"product_id": 1, "name": "...", "price": "1000.00", "pv": 750, "quantity": 2, "image": "/media/..."},
            "3": {"product_id": 3, "name": "...", "price": "1000.00", "pv": 750, "quantity": 1, "image": None},
        }
    }

Keys are product_id (str) for fast lookup.
"""
from decimal import Decimal
from django.conf import settings
from products.models import Product


CART_SESSION_KEY = 'enerpulse_cart'


def get_cart(request):
    """Get the cart dict from session, initializing if needed."""
    if CART_SESSION_KEY not in request.session:
        request.session[CART_SESSION_KEY] = {'items': {}}
    return request.session[CART_SESSION_KEY]


def save_cart(request, cart):
    """Save cart back to session and mark as modified."""
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def add_to_cart(request, product_id, quantity=1):
    """
    Add a product to the cart.
    Returns (success, message_or_cart_summary).
    """
    cart = get_cart(request)
    pid = str(product_id)

    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return False, 'Product not found'

    if pid in cart['items']:
        cart['items'][pid]['quantity'] += quantity
    else:
        cart['items'][pid] = {
            'product_id': product.id,
            'name': product.get_name(),
            'price': str(product.price_usd),
            'pv': product.pv,
            'quantity': quantity,
            'image': product.image.url if product.image else None,
        }

    save_cart(request, cart)
    return True, get_cart_summary(cart)


def update_quantity(request, product_id, quantity):
    """Update the quantity of a cart item. If quantity <= 0, remove it."""
    cart = get_cart(request)
    pid = str(product_id)

    if pid not in cart['items']:
        return False, 'Item not in cart'

    if quantity <= 0:
        del cart['items'][pid]
    else:
        cart['items'][pid]['quantity'] = quantity

    save_cart(request, cart)
    return True, get_cart_summary(cart)


def remove_from_cart(request, product_id):
    """Remove an item from the cart."""
    cart = get_cart(request)
    pid = str(product_id)

    if pid in cart['items']:
        del cart['items'][pid]
        save_cart(request, cart)
        return True, get_cart_summary(cart)

    return False, 'Item not in cart'


def clear_cart(request):
    """Empty the entire cart."""
    if CART_SESSION_KEY in request.session:
        del request.session[CART_SESSION_KEY]
        request.session.modified = True
    return True, get_empty_summary()


def get_cart_summary(cart):
    """Calculate cart totals: count, subtotal, total_pv."""
    items = cart.get('items', {})
    count = sum(item['quantity'] for item in items.values())
    subtotal = sum(Decimal(item['price']) * item['quantity'] for item in items.values())
    total_pv = sum(item['pv'] * item['quantity'] for item in items.values())

    return {
        'count': count,
        'subtotal': str(subtotal),
        'total_pv': total_pv,
        'item_count': len(items),
    }


def get_empty_summary():
    return {'count': 0, 'subtotal': '0.00', 'total_pv': 0, 'item_count': 0}


def get_cart_items(request):
    """Get all items in the cart with product details."""
    cart = get_cart(request)
    items = cart.get('items', {}).values()
    return list(items)
