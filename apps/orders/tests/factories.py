from decimal import Decimal

import factory

from apps.orders.models import Order, OrderItem
from apps.products.tests.factories import ProductVariantFactory, UserFactory


class OrderFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)

    order_number = factory.Sequence(lambda n: f"ORD-{n:06}")

    status = Order.Status.PENDING

    payment_status = Order.PaymentStatus.PENDING

    subtotal = Decimal("100.00")

    total = Decimal("100.00")

    full_name = "John Doe"

    phone = "+8801712345678"

    address = "Dhaka"

    city = "Dhaka"

    postal_code = "1207"


class OrderItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)

    variant = factory.SubFactory(
        ProductVariantFactory,
    )

    product_name = factory.SelfAttribute(
        "variant.product.name",
    )

    sku = factory.SelfAttribute(
        "variant.sku",
    )

    size = factory.SelfAttribute(
        "variant.size",
    )

    color = factory.SelfAttribute(
        "variant.color",
    )

    price = factory.SelfAttribute(
        "variant.price",
    )

    quantity = 2

    total_price = Decimal("200.00")
