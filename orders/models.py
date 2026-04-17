from django.db import models
from django.conf import settings
from products.models import Product
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    """
    Represent the 'Headre' of a custumer purhase.
    Stores metadata, total coast, and delivery information.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PAID = 'PAID', _('Paid')
        SHIPPED = 'SHIPPED', _('Shipped')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELED = 'CANCELED', _('Canceled')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Customer')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Status')
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Total Price")
    )

    # Данные доставки (Snapshot на момент заказа)
    city = models.CharField(max_length=100, verbose_name=_('City'))
    address = models.TextField(verbose_name=_('Shipping Address'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self) -> str:
        return f"Order {self.pk} | {self.user.email}"


class OrderItem(models.Model):
    """
    Represent a specific product line within an Order.
    Crucial: Store 'price' as a snapshot to prevent historical data corruption.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_('Order')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_('Product')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
        help_text=_("Snapshot price at the moment of purchase")
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Quantity"),
    )

    def __str__(self) -> str:
        return f"Item {self.product.name} (x{self.quantity}) in Order {self.order_id}"

    def get_cost(self) -> Decimal:
        """Calculate total cost for this line item."""
        return self.price * self.quantity