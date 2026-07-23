from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.cart.models import CartItem
from apps.cart.services import (add_to_cart, clear_cart, get_or_create_cart,
                                remove_cart_item, update_cart_item)
from apps.products.tests.factories import ProductVariantFactory, UserFactory

from .factories import CartFactory, CartItemFactory


class CartServiceTest(TestCase):

    def test_get_or_create_cart_creates_new_cart(self):
        user = UserFactory()

        cart = get_or_create_cart(user)

        self.assertEqual(
            cart.user,
            user,
        )

    def test_get_or_create_cart_returns_existing_cart(self):
        cart = CartFactory()

        result = get_or_create_cart(
            cart.user,
        )

        self.assertEqual(
            result.id,
            cart.id,
        )

    def test_add_to_cart_creates_new_item(self):
        user = UserFactory()
        variant = ProductVariantFactory()

        cart = add_to_cart(
            user=user,
            variant=variant,
            quantity=2,
        )

        self.assertEqual(
            cart.items.count(),
            1,
        )

    def test_add_to_cart_increases_existing_quantity(self):
        user = UserFactory()
        variant = ProductVariantFactory()

        cart = CartFactory(
            user=user,
        )

        CartItemFactory(
            cart=cart,
            variant=variant,
            quantity=2,
        )

        add_to_cart(
            user=user,
            variant=variant,
            quantity=3,
        )

        item = CartItem.objects.get(
            cart=cart,
            variant=variant,
        )

        self.assertEqual(
            item.quantity,
            5,
        )

    def test_cannot_add_inactive_product(self):
        user = UserFactory()
        variant = ProductVariantFactory()

        variant.product.is_active = False
        variant.product.save()

        with self.assertRaises(
            ValidationError,
        ):
            add_to_cart(
                user=user,
                variant=variant,
                quantity=1,
            )

    def test_cannot_add_soft_deleted_product(self):
        user = UserFactory()
        variant = ProductVariantFactory()

        variant.product.deleted_at = timezone.now()
        variant.product.save()

        with self.assertRaises(
            ValidationError,
        ):
            add_to_cart(
                user=user,
                variant=variant,
                quantity=1,
            )

    def test_cannot_add_more_than_available_stock(self):
        user = UserFactory()

        variant = ProductVariantFactory(
            stock=5,
        )

        with self.assertRaises(
            ValidationError,
        ):
            add_to_cart(
                user=user,
                variant=variant,
                quantity=10,
            )

    def test_add_to_cart_returns_cart(self):
        user = UserFactory()
        variant = ProductVariantFactory()

        cart = add_to_cart(
            user=user,
            variant=variant,
            quantity=1,
        )

        self.assertEqual(
            cart.user,
            user,
        )

    def test_update_cart_item_quantity(self):
        cart_item = CartItemFactory(
            quantity=2,
        )

        update_cart_item(
            cart_item=cart_item,
            quantity=5,
        )

        cart_item.refresh_from_db()

        self.assertEqual(
            cart_item.quantity,
            5,
        )

    def test_update_cart_item_to_zero_deletes_item(self):
        cart_item = CartItemFactory()

        update_cart_item(
            cart_item=cart_item,
            quantity=0,
        )

        self.assertFalse(
            CartItem.objects.filter(
                id=cart_item.id,
            ).exists()
        )

    def test_update_cart_item_negative_quantity(self):
        cart_item = CartItemFactory()

        with self.assertRaises(
            ValidationError,
        ):
            update_cart_item(
                cart_item=cart_item,
                quantity=-1,
            )

    def test_update_cart_item_not_enough_stock(self):
        variant = ProductVariantFactory(
            stock=5,
        )

        cart_item = CartItemFactory(
            variant=variant,
            quantity=2,
        )

        with self.assertRaises(
            ValidationError,
        ):
            update_cart_item(
                cart_item=cart_item,
                quantity=10,
            )

    def test_remove_cart_item(self):
        cart_item = CartItemFactory()

        remove_cart_item(
            cart_item,
        )

        self.assertFalse(
            CartItem.objects.filter(
                id=cart_item.id,
            ).exists()
        )

    def test_remove_cart_item_deletes_only_one_item(self):
        cart = CartFactory()

        item1 = CartItemFactory(
            cart=cart,
        )

        CartItemFactory(
            cart=cart,
        )

        remove_cart_item(
            item1,
        )

        self.assertEqual(
            cart.items.count(),
            1,
        )

    def test_clear_cart(self):
        cart = CartFactory()

        CartItemFactory.create_batch(
            3,
            cart=cart,
        )

        clear_cart(
            cart,
        )

        self.assertEqual(
            cart.items.count(),
            0,
        )

    def test_clear_cart_empty_cart(self):
        cart = CartFactory()

        clear_cart(
            cart,
        )

        self.assertEqual(
            cart.items.count(),
            0,
        )
