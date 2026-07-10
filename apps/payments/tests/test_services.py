from django.test import TestCase
from unittest.mock import patch

from rest_framework.exceptions import ValidationError

from .base import BasePaymentTestCase

from apps.payments.models import Payment
from apps.payments.services import (
    create_payment,
    complete_payment,
    generate_transaction_id,
)

from apps.orders.models import Order


class PaymentServiceTest(BasePaymentTestCase):

    def setUp(self):
        super().setUp()

        self.payment.delete()

    def test_create_payment_success(self):

        payment = create_payment(
            user=self.user,
            order_id=self.order.id,
            provider=Payment.Provider.STRIPE,
        )

        self.assertEqual(
            payment.order,
            self.order,
        )

        self.assertEqual(
            payment.status,
            Payment.Status.PENDING,
        )

        self.assertEqual(
            payment.amount,
            self.order.total,
        )

    def test_cannot_create_duplicate_payment(self):

        Payment.objects.create(
            order=self.order,
            provider=Payment.Provider.STRIPE,
            transaction_id=generate_transaction_id(),
            amount=self.order.total,
        )

        with self.assertRaises(
            ValidationError,
        ):
            create_payment(
                user=self.user,
                order_id=self.order.id,
                provider=Payment.Provider.STRIPE,
            )

    def test_cannot_pay_paid_order(self):

        self.order.payment_status = (
            Order.PaymentStatus.PAID
        )
        self.order.save()

        with self.assertRaises(
            ValidationError,
        ):
            create_payment(
                user=self.user,
                order_id=self.order.id,
                provider=Payment.Provider.STRIPE,
            )

    def test_cannot_pay_cancelled_order(self):

        self.order.status = (
            Order.Status.CANCELLED
        )
        self.order.save()

        with self.assertRaises(
            ValidationError,
        ):
            create_payment(
                user=self.user,
                order_id=self.order.id,
                provider=Payment.Provider.STRIPE,
            )

    def test_complete_payment_success(self):

        payment = create_payment(
            user=self.user,
            order_id=self.order.id,
            provider=Payment.Provider.STRIPE,
        )

        payment = complete_payment(
            payment,
        )

        payment.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEqual(
            payment.status,
            Payment.Status.SUCCESS,
        )

        self.assertIsNotNone(
            payment.paid_at,
        )

        self.assertEqual(
            self.order.payment_status,
            Order.PaymentStatus.PAID,
        )

    def test_complete_payment_twice(self):

        payment = create_payment(
            user=self.user,
            order_id=self.order.id,
            provider=Payment.Provider.STRIPE,
        )

        complete_payment(payment)

        payment.refresh_from_db()

        paid_at = payment.paid_at

        payment = complete_payment(
            payment,
        )

        self.assertEqual(
            payment.paid_at,
            paid_at,
        )

    def test_generate_transaction_id(self):

        first = generate_transaction_id()

        second = generate_transaction_id()

        self.assertNotEqual(
            first,
            second,
        )

        self.assertTrue(
            first.startswith("TXN-"),
        )