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
        queryset.update(status='DELIVERED')

    # Аналитика в футере списка
    def changelist_view(self, request, extra_context=None):
        # 1. Сначала готовим контекст (ИСПРАВЛЕНО: правильное имя переменной)
        extra_context = extra_context or {}

        # 2. Делаем расчеты ДО вызова super()
        # Получаем текущий набор данных (с учетом фильтров админки)
        qs = self.get_queryset(request)

        # Считаем сумму
        revenue = qs.aggregate(Sum('total_price'))['total_price__sum']
        extra_context['total_revenue'] = revenue or 0  # Добавили or 0 на случай пустой базы

        # 3. Вызываем super() ОДИН РАЗ в самом конце
        return super().changelist_view(request, extra_context=extra_context)
