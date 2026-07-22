from apps.payments.selectors import get_user_payments
from apps.products.tests.factories import UserFactory

from .base import BasePaymentTestCase
from .factories import PaymentFactory


class PaymentSelectorTest(BasePaymentTestCase):

    def test_get_user_payments(self):

        payments = get_user_payments(
            self.user,
        )

        self.assertEqual(
            payments.count(),
            1,
        )

        self.assertEqual(
            payments.first(),
            self.payment,
        )

    def test_returns_only_user_payments(self):

        other_user = UserFactory()

        PaymentFactory(
            order__user=other_user,
        )

        payments = get_user_payments(
            self.user,
        )

        self.assertEqual(
            payments.count(),
            1,
        )

        self.assertEqual(
            payments.first(),
            self.payment,
        )

    def test_empty_queryset(self):

        self.payment.delete()

        payments = get_user_payments(
            self.user,
        )

        self.assertEqual(
            payments.count(),
            0,
        )
