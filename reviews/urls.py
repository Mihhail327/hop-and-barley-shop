from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    # Путь для добавления отзыва к конкретному товару по его ID
    path('add/<int:product_id>/', views.add_review, name='add_review'),
]
