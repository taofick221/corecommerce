from django.urls import reverse
from rest_framework.test import APITestCase

from apps.orders.tests.factories import (
    OrderFactory,
)

from .factories import (
    PaymentFactory,
)


class BasePaymentTestCase(APITestCase):

    def setUp(self):

        self.order = OrderFactory()

        self.user = self.order.user

        self.payment = PaymentFactory(
            order=self.order,
        )

        self.payments_url = reverse(
            "payments",
        )

        self.payment_detail_url = reverse(
            "payment_detail",
            kwargs={
                "payment_id": self.payment.id,
            },
        )

        self.create_payment_url = reverse(
            "create_payment",
            kwargs={
                "order_id": self.order.id,
            },
        )