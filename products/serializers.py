from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'name_en', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для красивого вывода категории
    category = CategorySerializer(read_only=True)

    # Кастомное поле: статус наличия текстом
    availability_status = serializers.SerializerMethodField()

    # Ссылка на изображение (чтобы всегда был полный URL с http://...)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name_ru', 'name_en', 'price',
            'stock', 'availability_status', 'category', 'image_url'
        ]

    def get_availability_status(self, obj):
        """Логика для отображения статуса запасов"""
        if obj.stock > 10:
            return "High Stock"
        if obj.stock > 0:
            return f"Low Stock ({obj.stock} left)"
        return "Out of Stock"

    def get_image_url(self, obj):
        """Гарантируем получение полного пути к картинке"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def validate_price(self, value):
        """Бизнес-валидация: цена не может быть нулевой или отрицательной"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        """Бизнес-валидация: остатки не могут быть меньше нуля"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
