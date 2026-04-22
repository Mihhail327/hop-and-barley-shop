from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.models import Product


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Добавляем валидаторы, чтобы оценка была строго от 1 до 5
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment_ru = models.TextField(verbose_name="Комментарий (RU)")
    comment_en = models.TextField(blank=True, verbose_name="Comment (EN)")

    @property
    def comment(self):
        from django.utils.translation import get_language
        val = self.comment_ru if get_language() == 'ru' else self.comment_en
        return val or self.comment_ru
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # Гарантируем, что один пользователь может оставить только один отзыв на один товар
        unique_together = ('product', 'user')

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'
