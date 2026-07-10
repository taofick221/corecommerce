from rest_framework import status

from .base import BasePaymentTestCase

from apps.payments.models import Payment
from apps.orders.models import Order
from apps.products.tests.factories import UserFactory
from apps.orders.tests.factories import OrderFactory


class CreatePaymentAPITest(BasePaymentTestCase):

    def setUp(self):
        super().setUp()
        self.payment.delete()

    def test_create_payment_success(self):

        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.create_payment_url,
            {
                "provider": Payment.Provider.STRIPE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_requires_authentication(self):

        response = self.client.post(
            self.create_payment_url,
            {
                "provider": Payment.Provider.STRIPE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_invalid_provider(self):

        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.create_payment_url,
            {
                "provider": "paypal",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_payment(self):

        self.payment = Payment.objects.create(
            order=self.order,
            provider=Payment.Provider.STRIPE,
            transaction_id="TXN123456",
            amount=self.order.total,
        )

        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.create_payment_url,
            {
                "provider": Payment.Provider.STRIPE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_paid_order(self):

        self.order.payment_status = Order.PaymentStatus.PAID
        self.order.save()

        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.create_payment_url,
            {
                "provider": Payment.Provider.STRIPE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cancelled_order(self):

        self.order.status = Order.Status.CANCELLED
        self.order.save()

        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.create_payment_url,
            {
                "provider": Payment.Provider.STRIPE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class PaymentListAPITest(BasePaymentTestCase):

    def test_get_payments(self):

        self.client.force_authenticate(self.user)

        response = self.client.get(
            self.payments_url,
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
            self.payments_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_empty_payment_list(self):

        self.payment.delete()

        self.client.force_authenticate(self.user)

        response = self.client.get(
            self.payments_url,
        )

        self.assertEqual(
            len(response.data),
            0,
        )


class PaymentDetailAPITest(BasePaymentTestCase):

    def test_get_payment(self):

        self.client.force_authenticate(self.user)

        response = self.client.get(
            self.payment_detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["transaction_id"],
            self.payment.transaction_id,
        )

    def test_requires_authentication(self):

        response = self.client.get(
            self.payment_detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_other_user_cannot_access_payment(self):

        other_user = UserFactory()

        other_order = OrderFactory(
            user=other_user,
        )

        other_payment = Payment.objects.create(
            order=other_order,
            provider=Payment.Provider.STRIPE,
            transaction_id="TXN999999",
            amount=other_order.total,
        )

        self.client.force_authenticate(self.user)

        response = self.client.get(
            f"/api/payments/{other_payment.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_invalid_payment_id(self):

        self.client.force_authenticate(self.user)

        response = self.client.get(
            "/api/payments/99999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )