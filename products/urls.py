from django.urls import path
from django.views.generic import TemplateView

from .views import ProductDetailView, ProductListView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('guides/', TemplateView.as_view(template_name='guides-recipes.html'), name='guides_recipes'),
]
