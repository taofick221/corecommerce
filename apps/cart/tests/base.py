from django.urls import reverse
from rest_framework.test import APITestCase

from apps.products.tests.factories import (ProductFactory,
                                           ProductVariantFactory, UserFactory)

from .factories import CartFactory, CartItemFactory


class BaseCartTestCase(APITestCase):

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

        self.cart_url = reverse(
            "cart",
        )

        self.add_to_cart_url = reverse(
            "add_to_cart",
        )

        self.update_cart_item_url = reverse(
            "update_cart_item",
            kwargs={
                "item_id": self.cart_item.id,
            },
        )

        self.remove_cart_item_url = reverse(
            "remove_cart_item",
            kwargs={
                "item_id": self.cart_item.id,
            },
        )

        self.clear_cart_url = reverse(
            "clear_cart",
        )
