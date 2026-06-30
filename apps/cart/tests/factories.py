import factory

from apps.cart.models import (
    Cart,
    CartItem,
)

from apps.products.tests.factories import (
    UserFactory,
    ProductVariantFactory,
)


class CartFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Cart

    user = factory.SubFactory(
        UserFactory,
    )


class CartItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CartItem

    cart = factory.SubFactory(
        CartFactory,
    )

    variant = factory.SubFactory(
        ProductVariantFactory,
    )

    quantity = 2