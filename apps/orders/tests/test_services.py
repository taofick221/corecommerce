from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from unittest.mock import patch

from .base import BaseOrderTestCase

from apps.orders.services import create_order
from apps.orders.models import Order
from apps.orders.tests.factories import OrderItemFactory


class OrderServiceTest(BaseOrderTestCase):

    @patch("apps.orders.services.send_order_confirmation_email.delay")
    def test_create_order_success(self, mock_delay):

        shipping_data = {
            "full_name": "John Doe",
            "phone": "+8801712345678",
            "address": "Dhaka",
            "city": "Dhaka",
            "postal_code": "1207",
        }

        order = create_order(
            self.user,
            shipping_data,
        )

        self.assertEqual(
            order.user,
            self.user,
        )

        self.assertEqual(
            order.items.count(),
            1,
        )

        self.assertEqual(
            order.status,
            Order.Status.PENDING,
        )

        self.assertEqual(
            self.cart.items.count(),
            0,
        )

        mock_delay.assert_called_once_with(
            order.id,
        )

    @patch("apps.orders.services.send_order_confirmation_email.delay")
    def test_empty_cart_cannot_create_order(self, mock_delay):

        self.cart.items.all().delete()

        shipping_data = {
            "full_name": "John Doe",
            "phone": "+8801712345678",
            "address": "Dhaka",
            "city": "Dhaka",
            "postal_code": "1207",
        }

        with self.assertRaises(
            ValidationError,
        ):
            create_order(
                self.user,
                shipping_data,
            )

        mock_delay.assert_not_called()

    @patch("apps.orders.services.send_order_confirmation_email.delay")
    def test_inactive_product_cannot_create_order(
        self,
        mock_delay,
    ):

        self.product.is_active = False
        self.product.save()

        shipping_data = {
            "full_name": "John Doe",
            "phone": "+8801712345678",
            "address": "Dhaka",
            "city": "Dhaka",
            "postal_code": "1207",
        }

        with self.assertRaises(
            ValidationError,
        ):
            create_order(
                self.user,
                shipping_data,
            )

        mock_delay.assert_not_called()

    @patch("apps.orders.services.send_order_confirmation_email.delay")
    def test_soft_deleted_product_cannot_create_order(
        self,
        mock_delay,
    ):

        self.product.deleted_at = timezone.now()
        self.product.save()

        shipping_data = {
            "full_name": "John Doe",
            "phone": "+8801712345678",
            "address": "Dhaka",
            "city": "Dhaka",
            "postal_code": "1207",
        }

        with self.assertRaises(
            ValidationError,
        ):
            create_order(
                self.user,
                shipping_data,
            )

        mock_delay.assert_not_called()

    @patch("apps.orders.services.send_order_confirmation_email.delay")
    def test_not_enough_stock(
        self,
        mock_delay,
    ):

        self.variant.stock = 1
        self.variant.save()

        self.cart_item.quantity = 5
        self.cart_item.save()

        shipping_data = {
            "full_name": "John Doe",
            "phone": "+8801712345678",
            "address": "Dhaka",
            "city": "Dhaka",
            "postal_code": "1207",
        }

        with self.assertRaises(
            ValidationError,
        ):
            create_order(
                self.user,
                shipping_data,
            )

        mock_delay.assert_not_called()

    @patch("apps.orders.services.send_order_confirmation_email.delay")
    def test_stock_is_reduced_after_order(
        self,
        mock_delay,
    ):

        initial_stock = self.variant.stock

        shipping_data = {
            "full_name": "John Doe",
            "phone": "+8801712345678",
            "address": "Dhaka",
            "city": "Dhaka",
            "postal_code": "1207",
        }

        create_order(
            self.user,
            shipping_data,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.stock,
            initial_stock - self.cart_item.quantity,
        )

    @patch("apps.orders.services.send_order_confirmation_email.delay")
    def test_order_totals_are_correct(
        self,
        mock_delay,
    ):

        shipping_data = {
            "full_name": "John Doe",
            "phone": "+8801712345678",
            "address": "Dhaka",
            "city": "Dhaka",
            "postal_code": "1207",
        }

        order = create_order(
            self.user,
            shipping_data,
        )

        self.assertEqual(
            order.subtotal,
            order.total,
        )

    def test_generate_unique_order_number(self):
        from apps.orders.services import generate_order_number

        first = generate_order_number()
        second = generate_order_number()

        self.assertNotEqual(
            first,
            second,
        )

        self.assertTrue(
            first.startswith("ORD-"),
        )