from django.test import TestCase

from apps.cart.selectors import get_user_cart

from .factories import (
    CartFactory,
    CartItemFactory,
)


class CartSelectorTest(TestCase):

    def test_get_user_cart(self):
        cart = CartFactory()

        result = get_user_cart(
            cart.user,
        )

        self.assertEqual(
            result.id,
            cart.id,
        )

    def test_get_user_cart_returns_items(self):
        cart = CartFactory()

        CartItemFactory.create_batch(
            3,
            cart=cart,
        )

        result = get_user_cart(
            cart.user,
        )

        self.assertEqual(
            result.items.count(),
            3,
        )

    def test_get_user_cart_returns_correct_user(self):
        cart = CartFactory()

        result = get_user_cart(
            cart.user,
        )

        self.assertEqual(
            result.user,
            cart.user,
        )

    def test_get_user_cart_prefetches_variant(self):
        cart = CartFactory()

        item = CartItemFactory(
            cart=cart,
        )

        result = get_user_cart(
            cart.user,
        )

        self.assertEqual(
            result.items.first().variant.id,
            item.variant.id,
        )