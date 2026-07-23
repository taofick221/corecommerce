from django.test import TestCase

from apps.orders.serializers import (
    CreateOrderSerializer,
    OrderItemSerializer,
    OrderSerializer,
)

from .factories import OrderFactory, OrderItemFactory


class CreateOrderSerializerTest(TestCase):

    def test_valid_serializer(self):
        serializer = CreateOrderSerializer(
            data={
                "full_name": "John Doe",
                "phone": "+8801712345678",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            }
        )

        self.assertTrue(serializer.is_valid())

    def test_invalid_phone(self):
        serializer = CreateOrderSerializer(
            data={
                "full_name": "John Doe",
                "phone": "abc123",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            }
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "phone",
            serializer.errors,
        )

    def test_missing_required_field(self):
        serializer = CreateOrderSerializer(
            data={
                "phone": "+8801712345678",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            }
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "full_name",
            serializer.errors,
        )


class OrderItemSerializerTest(TestCase):

    def test_serializer_fields(self):
        item = OrderItemFactory()

        data = OrderItemSerializer(item).data

        self.assertEqual(
            data["product_name"],
            item.product_name,
        )

        self.assertEqual(
            data["sku"],
            item.sku,
        )

        self.assertEqual(
            int(data["quantity"]),
            item.quantity,
        )


class OrderSerializerTest(TestCase):

    def test_serializer_fields(self):
        order = OrderFactory()

        OrderItemFactory(order=order)

        data = OrderSerializer(order).data

        self.assertEqual(
            data["order_number"],
            order.order_number,
        )

        self.assertEqual(
            data["status"],
            order.status,
        )

        self.assertEqual(
            data["payment_status"],
            order.payment_status,
        )

        self.assertEqual(
            len(data["items"]),
            1,
        )

    def test_read_only_fields(self):
        serializer = OrderSerializer()

        self.assertIn(
            "order_number",
            serializer.Meta.read_only_fields,
        )

        self.assertIn(
            "status",
            serializer.Meta.read_only_fields,
        )

        self.assertIn(
            "payment_status",
            serializer.Meta.read_only_fields,
        )
