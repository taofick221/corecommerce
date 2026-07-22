from django.test import TestCase

from apps.products.views import ProductViewSet
from core.throttles import ProductRateThrottle


class ProductThrottleTest(TestCase):

    def test_list_uses_product_throttle(self):
        view = ProductViewSet()
        view.action = "list"

        throttles = view.get_throttles()

        self.assertEqual(len(throttles), 1)
        self.assertIsInstance(
            throttles[0],
            ProductRateThrottle,
        )

    def test_detail_uses_product_throttle(self):
        view = ProductViewSet()
        view.action = "retrieve"

        throttles = view.get_throttles()

        self.assertEqual(len(throttles), 1)
        self.assertIsInstance(
            throttles[0],
            ProductRateThrottle,
        )

    def test_create_uses_default_throttle(self):
        view = ProductViewSet()
        view.action = "create"

        throttles = view.get_throttles()

        self.assertIsInstance(
            throttles,
            list,
        )
