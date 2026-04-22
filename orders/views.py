from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product

from .cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


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
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                # Входим в атомарную транзакцию: либо всё сохранится, либо ничего
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_price = cart.get_total_price()
                    order.status = Order.Status.PAID  # Имитация оплаты
                    order.save()

                    subject = f'Заказ №{order.id} оформлен'
                    message = f'Привет, {request.user.username}! Твой заказ на сумму {order.total_price} принят.'
                    send_mail(
                        subject,
                        message,
                        'shop@hopandbarley.com',
                        [request.user.email, 'admin@hopandbarley.com'],  # Уведомляем обоих
                        fail_silently=False,
                    )

                    for item in cart:
                        product = item['product']
                        quantity = item['quantity']

                        # Валидация остатков (Select for update заблокирует строку в БД для безопасности)
                        product_in_db = Product.objects.select_for_update().get(id=product.id)

                        if product_in_db.stock < quantity:
                            raise ValueError(f"Недостаточно товара: {product.name_ru}")

                        # Списание
                        product_in_db.stock -= quantity
                        product_in_db.save()

                        OrderItem.objects.create(
                            order=order,
                            product=product_in_db,
                            price=item['price'],
                            quantity=quantity
                        )

                    cart.clear()
                    return render(request, 'orders/created.html', {'order': order})

            except ValueError as e:
                messages.error(request, str(e))
                return redirect('orders:cart_detail')
    else:
        form = OrderCreateForm()
    return render(request, 'checkout.html', {'cart': cart, 'form': form})
