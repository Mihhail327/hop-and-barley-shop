from rest_framework import viewsets, permissions
from orders.models import Order
from api.serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Пользователь видит только свои заказы
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Автоматически привязываем заказ к текущему пользователю
        serializer.save(user=self.request.user)