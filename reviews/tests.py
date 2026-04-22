import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

from orders.models import Order, OrderItem
from products.models import Category, Product
from reviews.models import Review


@pytest.mark.django_db
class TestReviewSystem:
    """Тестирование системы отзывов согласно ТЗ 3.2."""

    def setup_method(self):
        """Подготовка данных для тестов."""
        self.category = Category.objects.create(name_ru="Эль", slug="ale")
        self.product = Product.objects.create(
            name_ru="IPA",
            slug="ipa",
            price=250.00,
            stock=10,
            category=self.category
        )

    def test_review_forbidden_without_purchase(self, admin_client):
        """Тест: Нельзя оставить отзыв без покупки товара."""
        url = reverse('reviews:add_review', kwargs={'product_id': self.product.id})
        response = admin_client.post(url, {
            'rating': 5,
            'comment': 'Отличное пиво!'
        })

        # Должен быть редирект с ошибкой, а отзыв не должен создаться
        assert response.status_code == 302
        assert Review.objects.count() == 0

    def test_review_allowed_after_purchase(self, admin_user, admin_client):
        """Тест: Можно оставить отзыв после успешной оплаты заказа."""
        # Имитируем покупку
        order = Order.objects.create(user=admin_user, status='PAID', total_price=250.00)
        OrderItem.objects.create(order=order, product=self.product, price=250.00, quantity=1)

        url = reverse('reviews:add_review', kwargs={'product_id': self.product.id})
        response = admin_client.post(url, {
            'rating': 5,
            'comment': 'Теперь я могу оставить отзыв!'
        })

        assert response.status_code == 302
        assert Review.objects.filter(product=self.product, user=admin_user).exists()

    def test_review_rating_validation(self, admin_user, admin_client):
        """Тест: Рейтинг должен быть в пределах 1-5."""
        # Создаем запись о покупке
        order = Order.objects.create(user=admin_user, status='PAID', total_price=250.00)
        OrderItem.objects.create(order=order, product=self.product, price=250.00, quantity=1)

        # Пробуем поставить рейтинг 10 (валидаторы модели должны сработать)
        with pytest.raises(ValidationError):  # Модель выбросит ошибку при сохранении
            review = Review(
                product=self.product,
                user=admin_user,
                rating=10,
                comment_ru="Bad rating"
            )
            review.full_clean()
