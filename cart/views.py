from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .cart import add_to_cart, update_quantity, remove_from_cart, clear_cart, get_cart_items, get_cart_summary, get_cart


@csrf_exempt
@require_POST
def cart_add(request):
    """Add item to cart. POST {product_id, quantity (default 1)}"""
    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return JsonResponse({'error': 'product_id is required'}, status=400)

    success, result = add_to_cart(request, product_id, quantity)
    if not success:
        return JsonResponse({'error': result}, status=404)

    return JsonResponse(result)


@csrf_exempt
@require_POST
def cart_update(request):
    """Update item quantity. POST {product_id, quantity}"""
    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 0))

    if not product_id:
        return JsonResponse({'error': 'product_id is required'}, status=400)

    success, result = update_quantity(request, product_id, quantity)
    if not success:
        return JsonResponse({'error': result}, status=404)

    return JsonResponse(result)


@csrf_exempt
@require_POST
def cart_remove(request):
    """Remove item from cart. POST {product_id}"""
    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    product_id = data.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'product_id is required'}, status=400)

    success, result = remove_from_cart(request, product_id)
    if not success:
        return JsonResponse({'error': result}, status=404)

    return JsonResponse(result)


@csrf_exempt
@require_POST
def cart_clear(request):
    """Clear entire cart."""
    result = clear_cart(request)
    return JsonResponse(result)


def cart_view(request):
    """View cart contents."""
    items = get_cart_items(request)
    summary = get_cart_summary(get_cart(request) if hasattr(request, 'session') else {'items': {}})
    return JsonResponse({
        'items': items,
        'summary': summary,
    })
