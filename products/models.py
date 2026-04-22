from django.db import models
from django.utils.translation import get_language


class Category(models.Model):
    name_ru = models.CharField(max_length=255, verbose_name='Название (RU)')
    name_en = models.CharField(max_length=255, verbose_name='Name (EN)', blank=True)

    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-адрес (Slug)")

    description_ru = models.TextField(blank=True, verbose_name='Описание (RU)')
    description_en = models.TextField(blank=True, verbose_name='Description (EN)') # Убрали дубль blank=True

    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемая')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children', verbose_name='Родительская категория'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order', 'name_ru']

    @property
    def name(self):
        # Если английское имя пустое, отдаем русское как запасной вариант
        val = self.name_ru if get_language() == 'ru' else self.name_en
        return val or self.name_ru

    @property
    def description(self):
        val = self.description_ru if get_language() == 'ru' else self.description_en
        return val or self.description_ru

    def __str__(self):
        return self.name_ru


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория"
    )
    name_ru = models.CharField(max_length=255, verbose_name="Название (RU)")
    name_en = models.CharField(max_length=255, verbose_name="Name (EN)", blank=True) # Добавили blank=True

    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-адрес (Slug)")

    description_ru = models.TextField(blank=True, verbose_name="Описание (RU)")
    description_en = models.TextField(blank=True, verbose_name="Description (EN)") # Здесь blank=True уже был встроен в логику

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name='Порядок')
    image = models.ImageField(upload_to='products/', blank=True, verbose_name="Изображение")

    specifications = models.JSONField(default=dict, blank=True, verbose_name="Характеристики")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['order', '-created_at']

    @property
    def name(self):
        val = self.name_ru if get_language() == 'ru' else self.name_en
        return val or self.name_ru

    @property
    def description(self):
        val = self.description_ru if get_language() == 'ru' else self.description_en
        return val or self.description_ru

    @property
    def get_specifications(self):
        lang = get_language()
        if lang in self.specifications:
            return self.specifications[lang]
        # Fallback to returning all specifications if not structured by language
        return self.specifications


    def __str__(self):
        return self.name_ru
