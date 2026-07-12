from django.urls import reverse
from rest_framework.test import APITestCase

from apps.products.tests.factories import (
    UserFactory,
    ProductFactory,
    ProductVariantFactory,
)

from apps.cart.tests.factories import (
    CartFactory,
    CartItemFactory,
)

from .factories import (
    OrderFactory,
    OrderItemFactory,
)


class BaseOrderTestCase(APITestCase):

    def setUp(self):

        self.user = UserFactory()

        self.product = ProductFactory()

        self.variant = ProductVariantFactory(
            product=self.product,
        )

        self.cart = CartFactory(
            user=self.user,
        )

        self.cart_item = CartItemFactory(
            cart=self.cart,
            variant=self.variant,
        )

        self.order = OrderFactory(
            user=self.user,
        )

        self.order_item = OrderItemFactory(
            order=self.order,
            variant=self.variant,
        )

        self.create_order_url = reverse(
            "create_order",
        )

        self.orders_url = reverse(
            "orders",
        )

        self.order_detail_url = reverse(
            "order_detail",
            kwargs={
                "order_id": self.order.id,
            },
        )