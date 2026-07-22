from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.coupons.models import Coupon
from apps.coupons.services import calculate_coupon_discount

from .base import BaseCouponTestCase


class CouponServiceTest(BaseCouponTestCase):

    def test_percentage_discount(self):

        discount = calculate_coupon_discount(
            coupon=self.coupon,
            subtotal=Decimal("1000.00"),
        )

        self.assertEqual(
            discount,
            Decimal("100.00"),
        )

    def test_fixed_discount(self):

        self.coupon.discount_type = Coupon.DiscountType.FIXED

        self.coupon.discount_value = Decimal("200.00")

        self.coupon.save()

        discount = calculate_coupon_discount(
            coupon=self.coupon,
            subtotal=Decimal("1000.00"),
        )

        self.assertEqual(
            discount,
            Decimal("200.00"),
        )

    def test_maximum_discount_limit(self):

        self.coupon.discount_value = Decimal("50.00")

        self.coupon.maximum_discount_amount = Decimal("300.00")

        self.coupon.save()

        discount = calculate_coupon_discount(
            coupon=self.coupon,
            subtotal=Decimal("1000.00"),
        )

        self.assertEqual(
            discount,
            Decimal("300.00"),
        )

    def test_discount_never_exceeds_subtotal(self):

        self.coupon.discount_type = Coupon.DiscountType.FIXED

        self.coupon.discount_value = Decimal("5000.00")

        self.coupon.save()

        discount = calculate_coupon_discount(
            coupon=self.coupon,
            subtotal=Decimal("1000.00"),
        )

        self.assertEqual(
            discount,
            Decimal("1000.00"),
        )

    def test_coupon_not_found(self):

        with self.assertRaises(
            ValidationError,
        ):
            calculate_coupon_discount(
                coupon=None,
                subtotal=Decimal("1000.00"),
            )

    def test_inactive_coupon(self):

        self.coupon.is_active = False
        self.coupon.save()

        with self.assertRaises(
            ValidationError,
        ):
            calculate_coupon_discount(
                coupon=self.coupon,
                subtotal=Decimal("1000.00"),
            )

    def test_expired_coupon(self):

        self.coupon.valid_to = timezone.now() - timedelta(days=1)

        self.coupon.save()

        with self.assertRaises(
            ValidationError,
        ):
            calculate_coupon_discount(
                coupon=self.coupon,
                subtotal=Decimal("1000.00"),
            )

    def test_coupon_usage_limit_reached(self):

        self.coupon.used_count = 100
        self.coupon.usage_limit = 100
        self.coupon.save()

        with self.assertRaises(
            ValidationError,
        ):
            calculate_coupon_discount(
                coupon=self.coupon,
                subtotal=Decimal("1000.00"),
            )

    def test_minimum_order_amount(self):

        with self.assertRaises(
            ValidationError,
        ):
            calculate_coupon_discount(
                coupon=self.coupon,
                subtotal=Decimal("50.00"),
            )
