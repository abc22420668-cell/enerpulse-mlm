from .cart import get_cart_summary, CART_SESSION_KEY


def cart_count(request):
    """提供購物車數量給所有模板（導航列顯示）。"""
    cart = request.session.get(CART_SESSION_KEY, {'items': {}})
    summary = get_cart_summary(cart)
    return {'cart_item_count': summary['count']}
