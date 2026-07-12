from django.test import TestCase

from apps.payments.models import Payment
from apps.payments.serializers import (
    CreatePaymentSerializer,
    PaymentSerializer,
)

from .factories import PaymentFactory


class CreatePaymentSerializerTest(TestCase):

    def test_valid_serializer(self):

        serializer = CreatePaymentSerializer(
            data={
                "provider": Payment.Provider.STRIPE,
            }
        )

        self.assertTrue(
            serializer.is_valid()
        )

    def test_invalid_provider(self):

        serializer = CreatePaymentSerializer(
            data={
                "provider": "paypal",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "provider",
            serializer.errors,
        )


class PaymentSerializerTest(TestCase):

    def test_serializer_fields(self):

        payment = PaymentFactory()

        data = PaymentSerializer(
            payment
        ).data

        self.assertEqual(
            data["order_id"],
            payment.order.id,
        )

        self.assertEqual(
            data["order_number"],
            payment.order.order_number,
        )

        self.assertEqual(
            data["provider"],
            payment.provider,
        )

        self.assertEqual(
            data["status"],
            payment.status,
        )

        self.assertEqual(
            data["transaction_id"],
            payment.transaction_id,
        )

    def test_read_only_fields(self):

        serializer = PaymentSerializer()

        self.assertIn(
            "status",
            serializer.Meta.read_only_fields,
        )

        self.assertIn(
            "transaction_id",
            serializer.Meta.read_only_fields,
        )

        self.assertIn(
            "amount",
            serializer.Meta.read_only_fields,
        )

        self.assertIn(
            "paid_at",
            serializer.Meta.read_only_fields,
        )