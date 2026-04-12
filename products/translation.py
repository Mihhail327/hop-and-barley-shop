from modeltranslation.translator import register, TranslationOptions
from .models import Product, Category

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
