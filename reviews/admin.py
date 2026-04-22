from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['comment_ru', 'comment_en', 'product__name', 'user__email']
    # product__name и user__email позволяют искать по связанным полям
