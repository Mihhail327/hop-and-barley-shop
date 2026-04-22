from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Product


def index(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['products/includes/product_grid.html']
        return ['products/product_list.html']

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name_ru__icontains=query) |
                Q(name_en__icontains=query) |
                Q(description_ru__icontains=query) |
                Q(description_en__icontains=query)
            )

        types = self.request.GET.getlist('type')
        if types:
            queryset = queryset.filter(category__slug__in=types)

        sort = self.request.GET.get('sort', 'new')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем отзывы к контексту страницы
        context['reviews'] = self.object.reviews.all().order_by('-created_at')

        # Проверка: купил ли пользователь этот товар (для отображения формы отзыва)
        if self.request.user.is_authenticated:
            context['has_purchased'] = True
        return context
