from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id: int):
    """Controller to add or update items in the session-based cart."""
    cart = Cart(request)
    # Ищем продукт или возвращаем 404, если ID подделан
    product = get_object_or_404(Product, id=product_id)

    # В будущем здесь можно будет принимать количество из формы
    cart.add(product=product, quantity=1)

    return redirect('orders:cart_detail')

def cart_remove(request, product_id: int):
    """Controller to remove an item from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('orders:cart_detail')

def cart_detail(request):
    """Display the current state of the shopping cart."""
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})
