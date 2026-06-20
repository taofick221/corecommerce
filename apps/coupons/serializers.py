from rest_framework import serializers

from .models import Coupon


class CouponSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Coupon

        fields = [
            "id",
            "code",
            "discount_type",
            "discount_value",
            "minimum_order_amount",
            "maximum_discount_amount",
            "usage_limit",
            "used_count",
            "is_active",
            "valid_from",
            "valid_to",
        ]