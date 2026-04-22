import graphene
from graphene_django import DjangoObjectType
from products.models import Product, Category # Импортируй модель категории

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name_ru", "name_en")

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        # Используем список, это надежнее
        fields = ["id", "name_ru", "name_en", "description", "price", "category"]

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product_by_id = graphene.Field(ProductType, id=graphene.Int())

    def resolve_all_products(root, info):
        # Используем select_related для оптимизации (чтобы не было N+1 запросов)
        return Product.objects.select_related('category').all()

    def resolve_product_by_id(root, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)