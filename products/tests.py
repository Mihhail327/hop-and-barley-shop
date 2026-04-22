import pytest
from django.urls import reverse

from products.models import Category, Product


@pytest.mark.django_db
class TestProductCatalog:
    """Тестирование каталога товаров согласно ТЗ 3.1 и 3.2."""

    def setup_method(self):
        """Создание базовых данных: категории и товаров."""
        self.category = Category.objects.create(name_ru="Солод", slug="malt")
        self.product_1 = Product.objects.create(
            name_ru="Базовый солод",
            slug="base-malt",
            description_ru="Отличный солод для лагера",
            price=150.00,
            stock=100,
            category=self.category,
            is_active=True
        )
        self.product_2 = Product.objects.create(
            name_ru="Карамельный солод",
            slug="caramel-malt",
            description_ru="Для цвета и вкуса",
            price=250.00,
            stock=50,
            category=self.category,
            is_active=True
        )

    def test_product_list_view(self, client):
        """Тест: Главная страница каталога доступна и отображает товары."""
        url = reverse('products:product_list')
        response = client.get(url)
        assert response.status_code == 200
        assert "Базовый солод" in response.content.decode()
        assert "Карамельный солод" in response.content.decode()

    def test_product_detail_view(self, client):
        """Тест: Страница товара доступна по slug."""
        url = reverse('products:product_detail', kwargs={'slug': self.product_1.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert self.product_1.description in response.content.decode()

    def test_product_search(self, client):
        """Тест: Поиск находит товар по названию."""
        url = reverse('products:product_list')
        response = client.get(url, {'q': 'Карамельный'})
        assert "Карамельный солод" in response.content.decode()
        assert "Базовый солод" not in response.content.decode()

    def test_category_filter(self, client):
        """Тест: Фильтрация товаров по категории."""
        new_cat = Category.objects.create(name_ru="Хмель", slug="hops")
        Product.objects.create(
            name_ru="Citra", slug="citra", price=500, stock=10, category=new_cat, is_active=True
        )

        url = reverse('products:product_list')
        response = client.get(url, {'type': 'hops'})
        assert "Citra" in response.content.decode()
        assert "Базовый солод" not in response.content.decode()
