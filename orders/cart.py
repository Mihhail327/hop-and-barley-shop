from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    """
    Stateful shopping cart managed via Django sessions.

    Attributes:
        session (django.contrib.sessions.backends.base.SessionBase): The current user session.
        cart (dict): Dictionary storage for cart items, where key is product_id.
    """

    def __init__(self, request):
        """
        Initialize the shopping cart.

        Args:
            request (django.http.HttpRequest): The current HTTP request object.
        """
        # Получаем объект сессии из запроса
        self.session = request.session

        # Пытаемся достать корзину по ключу из настроек (CART_SESSION_ID)
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Если корзины в сессии нет — создаем пустой словарь и сохраняем его
            # Это происходит при первом добавлении товара новым пользователем
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.

        Args:
            product (products.models.Product): Product instance to add.
            quantity (int): Number of items. Defaults to 1.
            override_quantity (bool): If True, replaces current quantity with new one.
        """
        # Превращаем ID в строку, так как JSON ключи в сессии могут быть только строками
        product_id = str(product.id)

        if product_id not in self.cart:
            # Если товара нет — инициализируем структуру данных
            # Цену храним как строку для безопасной JSON-сериализации
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            # Режим "установить значение" (например, из выпадающего списка в корзине)
            self.cart[product_id]['quantity'] = quantity
        else:
            # Режим "добавить к существующему" (кнопка "Купить" в каталоге)
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Mark the session as modified to ensure it is saved to the database/cache.
        """
        # Django не видит изменений внутри вложенных словарей автоматически.
        # Этот флаг принудительно заставляет Django обновить сессию в конце запроса.
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart session.

        Args:
            product (products.models.Product): Product instance to remove.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and fetch products from the database.

        Yields:
            dict: Item data including 'product' (Model instance), 'total_price' (Decimal).
        """
        # Собираем все ID товаров, которые сейчас лежат в сессии
        product_ids = self.cart.keys()

        # Делаем ОДИН запрос к БД вместо множества (защита от проблемы N+1)
        products = Product.objects.filter(id__in=product_ids)

        # Клонируем данные сессии, чтобы не испортить оригинал при расчетах
        cart = self.cart.copy()

        # Наполняем временный словарь реальными объектами моделей из БД
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # Конвертируем цену из строки обратно в Decimal для точных расчетов
            item['price'] = Decimal(item['price'])
            # Считаем стоимость позиции "на лету"
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items currently in the cart.

        Returns:
            int: Sum of all quantities.
        """
        # Считаем общее кол-во единиц товара (например, 2 хмеля + 3 солода = 5)
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total cost of all items in the cart.

        Returns:
            Decimal: Cumulative cost of the entire cart.
        """
        # Суммируем произведения цены на количество по всей корзине
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove the cart from the session.
        """
        # Удаляем ключ корзины из словаря сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()