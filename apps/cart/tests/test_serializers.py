from django.test import TestCase

from rest_framework.exceptions import ValidationError

from apps.cart.serializers import (
    CartItemSerializer,
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
)

from .factories import (
    CartFactory,
    CartItemFactory,
)

from apps.products.tests.factories import (
    ProductVariantFactory,
)


class CartItemSerializerTest(TestCase):

    def test_cart_item_serializer_fields(self):
        serializer = CartItemSerializer()

        self.assertEqual(
            set(serializer.fields.keys()),
            {
                "id",
                "variant",
                "product_name",
                "sku",
                "size",
                "color",
                "unit_price",
                "quantity",
                "total_price",
                "available_stock",
            },
        )

    def test_cart_item_serializer_quantity(self):
        item = CartItemFactory(quantity=3)

        serializer = CartItemSerializer(item)

        self.assertEqual(
            serializer.data["quantity"],
            3,
        )

    def test_cart_item_serializer_variant(self):
        item = CartItemFactory()

        serializer = CartItemSerializer(item)

        self.assertEqual(
            serializer.data["variant"],
            item.variant.id,
        )

    def test_cart_item_serializer_product_name(self):
        item = CartItemFactory()

        serializer = CartItemSerializer(item)

        self.assertEqual(
            serializer.data["product_name"],
            item.variant.product.name,
        )

    def test_cart_item_serializer_available_stock(self):
        item = CartItemFactory()

        serializer = CartItemSerializer(item)

        self.assertEqual(
            serializer.data["available_stock"],
            item.variant.available_stock,
        )


class CartSerializerTest(TestCase):

    def test_cart_serializer_fields(self):
        serializer = CartSerializer()

        self.assertEqual(
            set(serializer.fields.keys()),
            {
                "id",
                "items",
                "subtotal",
                "total",
                "created_at",
                "updated_at",
            },
        )

    def test_cart_serializer_returns_subtotal(self):
        cart = CartFactory()

        CartItemFactory(
            cart=cart,
            quantity=2,
        )

        serializer = CartSerializer(cart)

        self.assertEqual(
            serializer.data["subtotal"],
            cart.subtotal,
        )

    def test_cart_serializer_returns_total(self):
        cart = CartFactory()

        CartItemFactory(
            cart=cart,
        )

        serializer = CartSerializer(cart)

        self.assertEqual(
            serializer.data["total"],
            cart.total,
        )


class AddToCartSerializerTest(TestCase):

    def test_valid_serializer(self):
        variant = ProductVariantFactory()

        serializer = AddToCartSerializer(
            data={
                "variant_id": variant.id,
                "quantity": 2,
            }
        )

        self.assertTrue(
            serializer.is_valid(),
        )

    def test_invalid_variant(self):
        serializer = AddToCartSerializer(
            data={
                "variant_id": 99999,
                "quantity": 1,
            }
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_inactive_product(self):
        variant = ProductVariantFactory()

        variant.product.is_active = False
        variant.product.save()

        serializer = AddToCartSerializer(
            data={
                "variant_id": variant.id,
                "quantity": 1,
            }
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_quantity_more_than_stock(self):
        variant = ProductVariantFactory(
            stock=5,
        )

        serializer = AddToCartSerializer(
            data={
                "variant_id": variant.id,
                "quantity": 10,
            }
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_quantity_less_than_one(self):
        variant = ProductVariantFactory()

        serializer = AddToCartSerializer(
            data={
                "variant_id": variant.id,
                "quantity": 0,
            }
        )

        self.assertFalse(
            serializer.is_valid(),
        )


class UpdateCartItemSerializerTest(TestCase):

    def test_valid_quantity(self):
        cart_item = CartItemFactory()

        serializer = UpdateCartItemSerializer(
            data={
                "quantity": 2,
            },
            context={
                "cart_item": cart_item,
            },
        )

        self.assertTrue(
            serializer.is_valid(),
        )

    def test_not_enough_stock(self):
        variant = ProductVariantFactory(
            stock=5,
        )

        cart_item = CartItemFactory(
            variant=variant,
        )

        serializer = UpdateCartItemSerializer(
            data={
                "quantity": 10,
            },
            context={
                "cart_item": cart_item,
            },
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_negative_quantity(self):
        cart_item = CartItemFactory()

        serializer = UpdateCartItemSerializer(
            data={
                "quantity": -1,
            },
            context={
                "cart_item": cart_item,
            },
        )

        self.assertFalse(
            serializer.is_valid(),
        )