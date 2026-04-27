from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['products/includes/product_grid.html']
        return ['products/product_list.html']

    def get_queryset(self):
        # 1. Фильтруем только активные товары
        queryset = Product.objects.filter(is_active=True)

        # 2. Поиск по названию и описанию
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name_ru__icontains=query) |
                Q(name_en__icontains=query) |
                Q(description_ru__icontains=query) |
                Q(description_en__icontains=query)
            )

        # 3. Фильтрация по категориям
        types = self.request.GET.getlist('type')
        if types:
            queryset = queryset.filter(category__slug__in=types)

        # 4. НОВОЕ: Фильтрация по диапазону цен
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # 5. Сортировка (включая популярность по количеству отзывов)
        sort = self.request.GET.get('sort', 'new')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'popular':
            from django.db.models import Count
            queryset = queryset.annotate(review_count=Count('reviews')).order_by('-review_count')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all().order_by('-created_at')

        #  Проверка факта покупки перед разрешением отзыва
        if self.request.user.is_authenticated:
            # Проверяем, есть ли завершенные заказы с этим товаром у пользователя
            has_bought = self.request.user.orders.filter(
                items__product=self.object,
                status='paid'  # Или другой статус завершенного заказа
            ).exists()
            context['has_purchased'] = has_bought
        else:
            context['has_purchased'] = False

        return context