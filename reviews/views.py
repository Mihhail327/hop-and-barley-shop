from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from orders.models import OrderItem
from .models import Review


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # 1. Проверяем, купил ли пользователь этот товар и оплачен ли заказ
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='PAID'
        ).exists()

        if not has_purchased:
            messages.error(request, "Вы можете оставить отзыв только после покупки товара.")
            return redirect('products:product_detail', slug=product.slug)

        # 2. Проверяем, не оставлял ли пользователь отзыв ранее
        if Review.objects.filter(product=product, user=request.user).exists():
            messages.warning(request, "Вы уже оставили отзыв на этот товар.")
            return redirect('products:product_detail', slug=product.slug)

        # 3. Получаем данные из формы
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            from django.utils.translation import get_language
            kwargs = {
                'product': product,
                'user': request.user,
                'rating': int(rating),
            }
            if get_language() == 'ru':
                kwargs['comment_ru'] = comment
            else:
                kwargs['comment_en'] = comment
            Review.objects.create(**kwargs)
            messages.success(request, "Спасибо! Ваш отзыв успешно добавлен.")
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")

    return redirect('products:product_detail', slug=product.slug)