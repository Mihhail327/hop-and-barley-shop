from django.contrib import admin
from django.db.models import Sum

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    # Кастомный экшен для массового обновления
    actions = ['make_delivered']

    @admin.action(description='Отметить как доставлено')
    def make_delivered(self, request, queryset):
        queryset.update(status='delivered')

    # Аналитика в футере списка
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        # Считаем общую выручку по отфильтрованным заказам
        extra_context = extra_context or {}
        extra_context['total_revenue'] = qs.aggregate(Sum('total_price'))['total_price__sum']
        return super().changelist_view(request, extra_context=extra_context)
