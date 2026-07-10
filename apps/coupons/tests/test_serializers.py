from django.test import TestCase
from decimal import Decimal

from apps.coupons.models import Coupon
from apps.coupons.serializers import CouponSerializer

from .factories import CouponFactory


class CouponSerializerTest(TestCase):

    def test_serializer_fields(self):

        coupon = CouponFactory()

        data = CouponSerializer(
            coupon
        ).data

        self.assertEqual(
            data["code"],
            coupon.code,
        )

        self.assertEqual(
            data["discount_type"],
            coupon.discount_type,
        )

        self.assertEqual(
            Decimal(data["discount_value"]),
            coupon.discount_value,
        )

        self.assertEqual(
            Decimal(data["minimum_order_amount"]),
            coupon.minimum_order_amount,
        )

        self.assertEqual(
            data["usage_limit"],
            coupon.usage_limit,
        )

        self.assertEqual(
            data["used_count"],
            coupon.used_count,
        )

        self.assertEqual(
            data["is_active"],
            coupon.is_active,
        )

    def test_read_only_fields(self):

        serializer = CouponSerializer()

        self.assertEqual(
            serializer.Meta.model,
            Coupon,
        )

        self.assertIn(
            "code",
            serializer.fields,
        )

        self.assertIn(
            "discount_type",
            serializer.fields,
        )

        self.assertIn(
            "discount_value",
            serializer.fields,
        )

        self.assertIn(
            "valid_from",
            serializer.fields,
        )

        self.assertIn(
            "valid_to",
            serializer.fields,
        )