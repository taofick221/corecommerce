from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from rest_framework import status

from apps.coupons.models import Coupon

from .base import BaseCouponTestCase


class ValidateCouponAPITest(BaseCouponTestCase):

    def test_validate_coupon_success(self):

        self.client.force_authenticate(
            self.user,
        )

        response = self.client.post(
            self.validate_coupon_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["coupon"],
            self.coupon.code,
        )

    def test_requires_authentication(self):

        response = self.client.post(
            self.validate_coupon_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_invalid_coupon(self):

        self.client.force_authenticate(
            self.user,
        )

        response = self.client.post(
            self.validate_coupon_url,
            {
                "code": "INVALID",
                "subtotal": Decimal("1000.00"),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_inactive_coupon(self):

        self.client.force_authenticate(
            self.user,
        )

        self.coupon.is_active = False
        self.coupon.save()

        response = self.client.post(
            self.validate_coupon_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_expired_coupon(self):

        self.client.force_authenticate(
            self.user,
        )

        self.coupon.valid_to = timezone.now() - timedelta(days=1)

        self.coupon.save()

        response = self.client.post(
            self.validate_coupon_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_usage_limit_reached(self):

        self.client.force_authenticate(
            self.user,
        )

        self.coupon.used_count = 100
        self.coupon.usage_limit = 100
        self.coupon.save()

        response = self.client.post(
            self.validate_coupon_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_minimum_order_amount(self):

        self.client.force_authenticate(
            self.user,
        )

        response = self.client.post(
            self.validate_coupon_url,
            {
                "code": self.coupon.code,
                "subtotal": Decimal("50.00"),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_percentage_discount(self):

        self.client.force_authenticate(
            self.user,
        )

        response = self.client.post(
            self.validate_coupon_url,
            {
                "code": self.coupon.code,
                "subtotal": Decimal("1000.00"),
            },
            format="json",
        )

        self.assertEqual(
            Decimal(str(response.data["discount"])),
            Decimal("100.00"),
        )

    def test_fixed_discount(self):

        self.client.force_authenticate(
            self.user,
        )

        self.coupon.discount_type = Coupon.DiscountType.FIXED

        self.coupon.discount_value = Decimal("250.00")

        self.coupon.save()

        response = self.client.post(
            self.validate_coupon_url,
            {
                "code": self.coupon.code,
                "subtotal": Decimal("1000.00"),
            },
            format="json",
        )

        self.assertEqual(
            Decimal(str(response.data["discount"])),
            Decimal("250.00"),
        )

    def test_case_insensitive_coupon(self):

        self.client.force_authenticate(
            self.user,
        )

        response = self.client.post(
            self.validate_coupon_url,
            {
                "code": self.coupon.code.lower(),
                "subtotal": Decimal("1000.00"),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
