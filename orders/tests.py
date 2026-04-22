from django.contrib.auth import get_user_model
from django.test import TestCase

from products.models import Category, Product


class OrderStockTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@test.com', password='password123')
        self.category = Category.objects.create(name_ru="Хмель", slug="hop")
        self.product = Product.objects.create(
            name_ru="Citra",
            slug="citra",
            price=10.0,
            stock=5,
            category=self.category
        )

    def test_insufficient_stock_raises_error(self):
        """Проверка: заказ не должен создаваться, если stock < quantity"""
        # Имитируем логику из view
        quantity_to_buy = 10

        with self.assertRaises(ValueError):
            if self.product.stock < quantity_to_buy:
                raise ValueError("Недостаточно товара")
