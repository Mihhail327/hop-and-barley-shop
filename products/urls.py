from django.urls import path
from .views import ProductListView, index

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('catalog/', ProductListView.as_view(), name='product_list'), # Каталог
]