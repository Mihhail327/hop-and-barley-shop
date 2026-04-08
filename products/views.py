from django.shortcuts import render
from .models import Product
from django.views.generic import ListView

def index(request):
    products = Product.objects.all()
    # Указываем home.html вместо index.html
    return render(request, 'home.html', {'products': products})

class ProductListView(ListView):
    model = Product
    # Указываем home.html вместо products/product_list.html
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by = 12