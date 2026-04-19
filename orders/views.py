from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from django.contrib.auth.decorators import login_required

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

@login_required
def order_create(request):
    """Handles the checkout proccess.
    Validates delivery data, saves the order, and migrates cart item to DB.
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1.Создаем объект заказа, но не сохраняем в БД сразуб
            # так как нам нужно привязать пользователя
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            # 2. Переносим товары из корзины в OrderItem
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # 3. Очищаем корзину в сессии
            cart.clear()

            # 4. Пока редиректим на успех (создадим страницу позже)
            return render(request, 'orders/created.html', {'order': order})
    else:
        # Если GET-запрос - просто показываем пустую форму
        form = OrderCreateForm()

    return render(request, 'checkout.html', {'cart': cart, 'form': form})
