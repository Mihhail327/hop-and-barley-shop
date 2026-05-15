from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.api_views import ProductViewSet
from orders.api_views import OrderViewSet
from users.api_views import UserRegisterView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='api-register'),
]