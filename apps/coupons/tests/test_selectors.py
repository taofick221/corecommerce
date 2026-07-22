from apps.coupons.selectors import get_coupon_by_code

from .base import BaseCouponTestCase
from .factories import CouponFactory


class CouponSelectorTest(BaseCouponTestCase):

    def test_get_coupon_by_code(self):

        coupon = get_coupon_by_code(
            self.coupon.code,
        )

        self.assertEqual(
            coupon,
            self.coupon,
        )

    def test_get_coupon_case_insensitive(self):

        coupon = get_coupon_by_code(
            self.coupon.code.lower(),
        )

        self.assertEqual(
            coupon,
            self.coupon,
        )

    def test_get_invalid_coupon(self):

        coupon = get_coupon_by_code(
            "INVALID123",
        )

        self.assertIsNone(
            coupon,
        )

    def test_inactive_coupon_returns_none(self):

        self.coupon.is_active = False
        self.coupon.save()

        coupon = get_coupon_by_code(
            self.coupon.code,
        )

        self.assertIsNone(
            coupon,
        )

    def test_returns_first_matching_coupon(self):

        CouponFactory(
            code="SAVE100",
        )

        coupon = get_coupon_by_code(
            "SAVE100",
        )

        self.assertEqual(
            coupon.code,
            "SAVE100",
        )
