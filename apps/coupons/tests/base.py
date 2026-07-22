from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase

from apps.products.tests.factories import UserFactory

from .factories import CouponFactory


class BaseCouponTestCase(APITestCase):

    def setUp(self):

        self.user = UserFactory()

        self.coupon = CouponFactory()

        self.validate_coupon_url = reverse(
            "validate_coupon",
        )

        self.valid_payload = {
            "code": self.coupon.code,
            "subtotal": Decimal("1000.00"),
        }
