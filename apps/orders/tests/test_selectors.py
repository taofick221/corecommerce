from django.core.exceptions import ObjectDoesNotExist

from apps.orders.selectors import get_user_orders, get_user_orders_by_id
from apps.orders.tests.factories import OrderFactory

from .base import BaseOrderTestCase


class OrderSelectorTest(BaseOrderTestCase):

    def test_get_user_orders(self):
        orders = get_user_orders(self.user)

        self.assertEqual(
            orders.count(),
            1,
        )

        self.assertEqual(
            orders.first(),
            self.order,
        )

    def test_get_user_orders_only_returns_user_orders(self):
        OrderFactory()

        orders = get_user_orders(self.user)

        self.assertEqual(
            orders.count(),
            1,
        )

    def test_get_user_order_by_id(self):
        order = get_user_orders_by_id(
            self.user,
            self.order.id,
        )

        self.assertEqual(
            order,
            self.order,
        )

    def test_get_user_order_by_invalid_id(self):
        with self.assertRaises(
            ObjectDoesNotExist,
        ):
            get_user_orders_by_id(
                self.user,
                99999,
            )
