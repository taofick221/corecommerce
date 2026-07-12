from django.utils import timezone
from rest_framework import status
from unittest.mock import patch

from .base import BaseOrderTestCase

from apps.orders.models import Order


class CreateOrderAPITest(BaseOrderTestCase):

    @patch("apps.orders.services.send_order_confirmation_email.delay")
    def test_create_order_success(self, mock_delay):

        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.create_order_url,
            {
                "full_name": "John Doe",
                "phone": "+8801712345678",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_requires_authentication(self):

        response = self.client.post(
            self.create_order_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_empty_cart(self):

        self.client.force_authenticate(self.user)

        self.cart.items.all().delete()

        response = self.client.post(
            self.create_order_url,
            {
                "full_name": "John Doe",
                "phone": "+8801712345678",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_phone(self):

        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.create_order_url,
            {
                "full_name": "John Doe",
                "phone": "123",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_inactive_product(self):

        self.client.force_authenticate(self.user)

        self.product.is_active = False
        self.product.save()

        response = self.client.post(
            self.create_order_url,
            {
                "full_name": "John Doe",
                "phone": "+8801712345678",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_soft_deleted_product(self):

        self.client.force_authenticate(self.user)

        self.product.deleted_at = timezone.now()
        self.product.save()

        response = self.client.post(
            self.create_order_url,
            {
                "full_name": "John Doe",
                "phone": "+8801712345678",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_not_enough_stock(self):

        self.client.force_authenticate(self.user)

        self.variant.stock = 1
        self.variant.save()

        self.cart_item.quantity = 5
        self.cart_item.save()

        response = self.client.post(
            self.create_order_url,
            {
                "full_name": "John Doe",
                "phone": "+8801712345678",
                "address": "Dhaka",
                "city": "Dhaka",
                "postal_code": "1207",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class OrderListAPITest(BaseOrderTestCase):

    def test_get_orders(self):

        self.client.force_authenticate(self.user)

        response = self.client.get(
            self.orders_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_requires_authentication(self):

        response = self.client.get(
            self.orders_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class OrderDetailAPITest(BaseOrderTestCase):

    def test_get_order(self):

        self.client.force_authenticate(self.user)

        response = self.client.get(
            self.order_detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["order_number"],
            self.order.order_number,
        )

    def test_requires_authentication(self):

        response = self.client.get(
            self.order_detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_cannot_access_other_users_order(self):

        from apps.products.tests.factories import UserFactory
        from apps.orders.tests.factories import OrderFactory

        other_user = UserFactory()

        other_order = OrderFactory(
            user=other_user,
        )

        self.client.force_authenticate(
            self.user,
        )

        response = self.client.get(
            f"/api/orders/{other_order.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_invalid_order_id(self):

        self.client.force_authenticate(
            self.user,
        )

        response = self.client.get(
            "/api/orders/99999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )