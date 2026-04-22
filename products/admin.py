from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Используем новые поля name_ru и name_en
    list_display = ('name_ru', 'name_en', 'slug', 'parent', 'created_at')
    # Slug теперь генерируем из русского названия (или английского, по желанию)
    prepopulated_fields = {'slug': ('name_ru',)}
    search_fields = ('name_ru', 'name_en')
    list_filter = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Показываем оба языка в списке товаров
    list_display = ('name_ru', 'name_en', 'price', 'category', 'is_active', 'stock', 'created_at')
    prepopulated_fields = {'slug': ('name_ru',)}
    search_fields = ('name_ru', 'name_en', 'description_ru', 'description_en')
    list_filter = ('category', 'is_active', 'created_at')
    list_editable = ('price', 'is_active', 'stock')
