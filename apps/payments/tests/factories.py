from decimal import Decimal

import factory

from apps.orders.tests.factories import OrderFactory
from apps.payments.models import Payment


class PaymentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Payment

    order = factory.SubFactory(OrderFactory)

    provider = Payment.Provider.STRIPE

    status = Payment.Status.PENDING

    transaction_id = factory.Sequence(lambda n: f"TXN-{n:012}")

    amount = Decimal("100.00")
