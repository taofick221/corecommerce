import factory

from apps.products.models import Brand, Category, Product, ProductImage, ProductVariant
from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@test.com")

    password = factory.PostGenerationMethodCall(
        "set_password",
        "Test123@",
    )


class AdminFactory(UserFactory):

    is_staff = True
    is_superuser = True


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class BrandFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f"Brand {n}")


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")

    description = factory.Faker("sentence")

    category = factory.SubFactory(CategoryFactory)

    brand = factory.SubFactory(BrandFactory)

    is_active = True


class ProductVariantFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)

    size = factory.Sequence(lambda n: str(42 + n))

    color = factory.Sequence(lambda n: f"Color {n}")

    price = 100

    stock = 10

    sku = factory.Sequence(lambda n: f"SKU{1000+n}")

    is_default = False


class ProductImageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)

    alt_text = ""

    order = factory.Sequence(lambda n: n)

    is_primary = False
